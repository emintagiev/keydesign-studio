/**
 * Настройка отправки квиз-заявки.
 *
 * Formspree (рекомендуется):
 * 1. https://formspree.io → форма → email key-des@mail.ru
 * 2. Скопировать URL вида https://formspree.io/f/xxxxxxxx
 * 3. Вставить в endpoint ниже
 *
 * Пока endpoint пустой - fallback на mailto:key-des@mail.ru
 */
window.KDS_BRIEF = {
  endpoint: ""
};
