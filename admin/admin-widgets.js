/* Key Design Studio - Decap CMS widgets: compress on upload + multi-select */

(function () {
  "use strict";

  var MAX_EDGE = 1920;
  var JPEG_QUALITY = 0.76;
  var IMAGE_EXT = /\.(jpe?g|png|webp|gif|heic|heif|bmp|tiff?)$/i;

  function slugifyName(name) {
    return String(name || "photo")
      .replace(/\.[^.]+$/, "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "") || "photo";
  }

  function formatKb(bytes) {
    return Math.max(1, Math.round(bytes / 1024)) + " KB";
  }

  function toArray(value) {
    if (!value) return [];
    if (typeof value.toJS === "function") return value.toJS();
    if (Array.isArray(value)) return value;
    return [value];
  }

  function getItemPath(item) {
    if (!item) return "";
    if (typeof item === "string") return item;
    if (typeof item.get === "function") {
      return item.get("image") || item.get("path") || "";
    }
    return item.image || item.path || "";
  }

  function normalizeGallery(value) {
    return toArray(value)
      .map(function (item) {
        return getItemPath(item);
      })
      .filter(Boolean);
  }

  function isImageFile(file) {
    if (!file || !file.name) return false;
    if (file.type && /^image\//.test(file.type)) return true;
    return IMAGE_EXT.test(file.name);
  }

  function uniqueOutputName(originalName, index, used) {
    var base = slugifyName(originalName);
    var candidate = base + ".jpg";
    if (index > 0 || used[candidate]) {
      candidate = base + "-" + String(index + 1) + ".jpg";
    }
    var n = index + 1;
    while (used[candidate]) {
      n += 1;
      candidate = base + "-" + String(n) + ".jpg";
    }
    used[candidate] = true;
    return candidate;
  }

  function readPathFromPersistResult(result) {
    if (!result) return "";
    if (result.payload && result.payload.path) return result.payload.path;
    if (result.path) return result.path;
    return "";
  }

  function entrySlug(entry) {
    if (!entry) return "";
    if (typeof entry.getIn === "function") {
      return entry.getIn(["data", "slug"]) || entry.get("slug") || "";
    }
    return entry.slug || "";
  }

  function buildPublicPath(field, fileName, entry) {
    var folder = "assets/projects";
    if (field && typeof field.get === "function") {
      folder = field.get("public_folder") || field.get("media_folder") || folder;
    }
    folder = String(folder).replace(/\/$/, "");
    var slug = entrySlug(entry);
    if (slug) {
      folder = folder
        .replace(/\{\{fields\.slug\}\}/g, slug)
        .replace(/\{\{slug\}\}/g, slug);
    }
    return folder + "/" + fileName;
  }

  function compressImage(file, outputName) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file);
      var img = new Image();

      img.onload = function () {
        URL.revokeObjectURL(url);
        var width = img.naturalWidth || img.width;
        var height = img.naturalHeight || img.height;
        var scale = Math.min(1, MAX_EDGE / Math.max(width, height));
        var targetW = Math.max(1, Math.round(width * scale));
        var targetH = Math.max(1, Math.round(height * scale));
        var canvas = document.createElement("canvas");
        canvas.width = targetW;
        canvas.height = targetH;
        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, targetW, targetH);

        canvas.toBlob(
          function (blob) {
            if (!blob) {
              reject(new Error("Не удалось сжать изображение"));
              return;
            }
            var outName = outputName || slugifyName(file.name) + ".jpg";
            resolve(new File([blob], outName, {
              type: "image/jpeg",
              lastModified: Date.now(),
            }));
          },
          "image/jpeg",
          JPEG_QUALITY
        );
      };

      img.onerror = function () {
        URL.revokeObjectURL(url);
        reject(new Error("Не удалось прочитать файл: " + file.name));
      };

      img.src = url;
    });
  }

  function persistCompressedFile(props, file) {
    if (typeof props.onPersistMedia !== "function") {
      return Promise.reject(new Error("Загрузка недоступна - обновите страницу админки"));
    }
    return props.onPersistMedia(file, { field: props.field }).then(function (result) {
      var path = readPathFromPersistResult(result) || buildPublicPath(props.field, file.name, props.entry);
      if (!path || path.indexOf("{{") !== -1) {
        throw new Error("Не удалось сохранить: " + file.name);
      }
      return path;
    });
  }

  function uploadFiles(props, files, onProgress) {
    var list = Array.prototype.slice.call(files).filter(isImageFile);

    if (!list.length) {
      return Promise.reject(
        new Error("Не найдено подходящих фото. Выберите JPG, PNG или HEIC")
      );
    }

    var done = 0;
    var paths = [];
    var usedNames = {};

    return list.reduce(function (chain, file, index) {
      return chain.then(function () {
        var outputName = uniqueOutputName(file.name, index, usedNames);
        return compressImage(file, outputName).then(function (compressed) {
          if (onProgress) {
            onProgress({
              phase: "upload",
              current: done + 1,
              total: list.length,
              name: compressed.name,
              originalSize: file.size,
              compressedSize: compressed.size,
            });
          }
          return persistCompressedFile(props, compressed).then(function (path) {
            done += 1;
            paths.push(path);
            if (onProgress) {
              onProgress({
                phase: "done-one",
                current: done,
                total: list.length,
                name: compressed.name,
                originalSize: file.size,
                compressedSize: compressed.size,
              });
            }
          });
        });
      });
    }, Promise.resolve()).then(function () {
      return paths;
    });
  }

  function renderPicker(label, opts) {
    return h(
      "label",
      { className: "kds-media__picker" + (opts.disabled ? " is-disabled" : "") },
      h("span", { className: "kds-media__btn" }, label),
      h("input", {
        type: "file",
        accept: opts.accept || "image/*",
        multiple: !!opts.multiple,
        className: "kds-media__picker-input",
        onChange: opts.onChange,
        disabled: opts.disabled,
      })
    );
  }

  var KdsImageControl = createClass({
    displayName: "KdsImageControl",

    getInitialState: function () {
      return { busy: false, status: "" };
    },

    handleRemove: function () {
      if (this.state.busy) return;
      this.props.onChange("");
    },

    handleFiles: function (event) {
      var input = event.target;
      var file = input.files && input.files[0];
      if (!file || this.state.busy) return;

      if (!isImageFile(file)) {
        input.value = "";
        this.setState({ status: "Выберите файл JPG, PNG или HEIC" });
        return;
      }

      var self = this;
      this.setState({ busy: true, status: "Сжимаем фото…" });

      compressImage(file)
        .then(function (compressed) {
          self.setState({
            status:
              "Загружаем " +
              formatKb(compressed.size) +
              " (было " +
              formatKb(file.size) +
              ")…",
          });
          return persistCompressedFile(self.props, compressed);
        })
        .then(function (path) {
          self.props.onChange(path);
          self.setState({ busy: false, status: "" });
        })
        .catch(function (err) {
          console.error(err);
          self.setState({
            busy: false,
            status: err && err.message ? err.message : "Ошибка загрузки",
          });
        })
        .finally(function () {
          input.value = "";
        });
    },

    renderPreview: function () {
      var value = this.props.value;
      if (!value) return null;

      var asset = this.props.getAsset(value, this.props.field);
      var src = asset && asset.url ? asset.url : value;

      return h(
        "div",
        { className: "kds-media__preview" },
        h("img", { src: src, alt: "", className: "kds-media__thumb" }),
        h("div", { className: "kds-media__path" }, value)
      );
    },

    render: function () {
      var busy = this.state.busy;

      return h(
        "div",
        { className: "kds-media" },
        this.renderPreview(),
        h(
          "div",
          { className: "kds-media__actions" },
          renderPicker(this.props.value ? "Заменить фото" : "Выбрать фото", {
            onChange: this.handleFiles,
            disabled: busy,
          }),
          this.props.value
            ? h(
                "button",
                {
                  type: "button",
                  className: "kds-media__btn kds-media__btn--ghost",
                  onClick: this.handleRemove,
                  disabled: busy,
                },
                "Удалить"
              )
            : null
        ),
        h(
          "p",
          { className: "kds-media__hint" },
          "Фото сжимается до " +
            MAX_EDGE +
            " px перед загрузкой - так Publish проходит быстрее."
        ),
        this.state.status
          ? h("p", { className: "kds-media__status" }, this.state.status)
          : null
      );
    },
  });

  var KdsGalleryControl = createClass({
    displayName: "KdsGalleryControl",

    getInitialState: function () {
      return { busy: false, status: "" };
    },

    handleRemoveAt: function (index) {
      if (this.state.busy) return;
      var items = normalizeGallery(this.props.value);
      items.splice(index, 1);
      this.props.onChange(items);
    },

    handleFiles: function (event) {
      var input = event.target;
      var files = input.files;
      if (!files || !files.length || this.state.busy) return;

      var self = this;
      var existing = normalizeGallery(this.props.value);

      this.setState({
        busy: true,
        status: "Выбрано файлов: " + files.length + ". Начинаем загрузку…",
      });

      uploadFiles(this.props, files, function (info) {
        if (info.phase === "upload") {
          self.setState({
            status:
              "Фото " +
              info.current +
              " из " +
              info.total +
              ": " +
              formatKb(info.compressedSize) +
              " (было " +
              formatKb(info.originalSize) +
              ")",
          });
        }
      })
        .then(function (paths) {
          self.props.onChange(existing.concat(paths));
          self.setState({
            busy: false,
            status: "Готово: добавлено " + paths.length + " фото",
          });
          setTimeout(function () {
            self.setState({ status: "" });
          }, 3000);
        })
        .catch(function (err) {
          console.error(err);
          self.setState({
            busy: false,
            status: err && err.message ? err.message : "Ошибка загрузки",
          });
        })
        .finally(function () {
          input.value = "";
        });
    },

    renderItems: function () {
      var items = normalizeGallery(this.props.value);
      var self = this;

      if (!items.length) {
        return h("p", { className: "kds-media__empty" }, "Пока нет фотографий");
      }

      return h(
        "div",
        { className: "kds-media__grid" },
        items.map(function (path, index) {
          var asset = self.props.getAsset(path, self.props.field);
          var src = asset && asset.url ? asset.url : path;
          return h(
            "div",
            { className: "kds-media__card", key: path + "-" + index },
            h("img", { src: src, alt: "", className: "kds-media__thumb" }),
            h(
              "button",
              {
                type: "button",
                className: "kds-media__remove",
                onClick: function () {
                  self.handleRemoveAt(index);
                },
                disabled: self.state.busy,
                "aria-label": "Удалить фото",
              },
              "×"
            )
          );
        })
      );
    },

    render: function () {
      var busy = this.state.busy;
      var count = normalizeGallery(this.props.value).length;

      return h(
        "div",
        { className: "kds-media kds-media--gallery" },
        this.renderItems(),
        h(
          "div",
          { className: "kds-media__actions" },
          renderPicker(count ? "Добавить ещё фото" : "Выбрать фотографии", {
            multiple: true,
            onChange: this.handleFiles,
            disabled: busy,
          })
        ),
        h(
          "p",
          { className: "kds-media__hint" },
          "Можно выделить сразу несколько файлов. Каждое фото сжимается до " +
            MAX_EDGE +
            " px перед загрузкой."
        ),
        this.state.status
          ? h("p", { className: "kds-media__status" }, this.state.status)
          : null
      );
    },
  });

  CMS.registerWidget("kds-image", KdsImageControl);
  CMS.registerWidget("kds-gallery", KdsGalleryControl);
})();
