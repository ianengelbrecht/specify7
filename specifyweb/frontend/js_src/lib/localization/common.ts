/**
 * Localization strings that are shared across components
 *
 * @module
 */

import { createDictionary } from './utils';

// Refer to "Guidelines for Programmers" in ./README.md before editing this file

export const commonText = createDictionary({
  specifySeven: {
    comment: `
      This is an example of how to provide comments. Comments are visible to
      translators.
    `,
    'en-us': 'Specify 7',
    'ru-ru': 'Specify 7',
    'es-es': 'Specify 7',
    'fr-fr': 'Specify 7',
    'uk-ua': 'Вкажіть 7',
    'de-ch': 'Specify 7',
  },
  no: {
    'en-us': 'No',
    'ru-ru': 'Нет',
    'es-es': 'No',
    'fr-fr': 'Non',
    'uk-ua': 'Немає',
    'de-ch': 'Nein',
  },
  cancel: {
    'en-us': 'Cancel',
    'ru-ru': 'Отмена',
    'es-es': 'Cancelar',
    'fr-fr': 'Annuler',
    'uk-ua': 'Скасувати',
    'de-ch': 'Abbrechen',
  },
  back: {
    'en-us': 'Back',
    'ru-ru': 'Назад',
    'es-es': 'Atrás',
    'fr-fr': 'Retour',
    'uk-ua': 'Виберіть файли або перетягніть їх сюди',
    'de-ch': 'Zurück',
  },
  skip: {
    'en-us': 'Skip',
    'ru-ru': 'Пропустить',
    'es-es': 'Omitir',
    'fr-fr': 'Passer',
    'uk-ua': 'Пропустити',
    'de-ch': 'Überspringen',
  },
  create: {
    'en-us': 'Create',
    'ru-ru': 'Создать',
    'es-es': 'Crear',
    'fr-fr': 'Créer',
    'uk-ua': 'Створити',
    'de-ch': 'Erstellen',
  },
  close: {
    'en-us': 'Close',
    'ru-ru': 'Закрыть',
    'es-es': 'Cerrar',
    'fr-fr': 'Fermer',
    'uk-ua': 'Закрити',
    'de-ch': 'Schliessen',
  },
  apply: {
    'en-us': 'Apply',
    'ru-ru': 'Применить',
    'es-es': 'Aplicar',
    'fr-fr': 'Appliquer',
    'uk-ua': 'Застосувати',
    'de-ch': 'Anwenden',
  },
  applyAll: {
    'en-us': 'Apply All',
    'ru-ru': 'Применить все',
    'es-es': 'Aplicar todo',
    'fr-fr': 'Tout appliquer',
    'uk-ua': 'Застосувати все',
    'de-ch': 'Alle Anwenden',
  },
  clearAll: {
    'en-us': 'Clear all',
    'ru-ru': 'Очистить все',
    'es-es': 'Borrar todo',
    'fr-fr': 'Tout effacer',
    'uk-ua': 'Очистити все',
    'de-ch': 'Alles löschen',
  },
  save: {
    'en-us': 'Save',
    'ru-ru': 'Сохранить',
    'es-es': 'Guardar',
    'fr-fr': 'Sauvegarder',
    'uk-ua': 'зберегти',
    'de-ch': 'Speichern',
  },
  add: {
    'en-us': 'Add',
    'ru-ru': 'Добавить',
    'es-es': 'Añadir',
    'fr-fr': 'Ajouter',
    'uk-ua': 'додати',
    'de-ch': 'Hinzufügen',
  },
  open: {
    'en-us': 'Open',
    'ru-ru': 'Открыть',
    'es-es': 'Abrir',
    'fr-fr': 'Ouvrir',
    'uk-ua': 'ВІДЧИНЕНО',
    'de-ch': 'Öffnen',
  },
  delete: {
    'en-us': 'Delete',
    'es-es': 'Eliminar',
    'fr-fr': 'Supprimer',
    'uk-ua': 'Видалити',
    'de-ch': 'Löschen',
    'ru-ru': 'Удалить',
  },
  next: {
    'en-us': 'Next',
    'ru-ru': 'Следующий',
    'es-es': 'Siguiente',
    'fr-fr': 'Suivant',
    'uk-ua': 'Далі',
    'de-ch': 'Weiter',
  },
  previous: {
    'en-us': 'Previous',
    'ru-ru': 'Предыдущий',
    'es-es': 'Anterior',
    'fr-fr': 'Précédent',
    'uk-ua': 'Попередній',
    'de-ch': 'Zurück',
  },
  tool: {
    'en-us': 'Tool',
    'ru-ru': 'Инструмент',
    'es-es': 'Herramienta',
    'fr-fr': 'Outil',
    'uk-ua': 'Завантаження…',
    'de-ch': 'Tool',
  },
  tools: {
    'en-us': 'Tools',
    'ru-ru': 'Инструменты',
    'es-es': 'Herramientas',
    'fr-fr': 'Outils',
    'uk-ua': 'Інструменти',
    'de-ch': 'Tools',
  },
  loading: {
    'en-us': 'Loading…',
    'ru-ru': 'Загрузка…',
    'es-es': 'Cargando…',
    'fr-fr': 'Chargement…',
    'uk-ua': 'Завантаження…',
    'de-ch': 'Laden …',
  },
  uploaded: {
    'en-us': 'Uploaded',
    'ru-ru': 'Загружено',
    'es-es': 'Subido',
    'fr-fr': 'Téléversé',
    'uk-ua': 'Завантажено',
    'de-ch': 'Hochgeladen',
  },
  remove: {
    'en-us': 'Remove',
    'ru-ru': 'Удалить',
    'es-es': 'Eliminar',
    'fr-fr': 'Retirer',
    'uk-ua': 'видалити',
    'de-ch': 'Entfernen',
  },
  search: {
    'en-us': 'Search',
    'ru-ru': 'Искать',
    'es-es': 'Buscar',
    'fr-fr': 'Recherche',
    'uk-ua': 'Пошук',
    'de-ch': 'Suche',
  },
  noResults: {
    'en-us': 'No Results',
    'ru-ru': 'Нет результатов',
    'es-es': 'Sin resultados',
    'fr-fr': 'Aucun résultat',
    'uk-ua': 'Немає результатів',
    'de-ch': 'Keine Resultate',
  },
  notApplicable: {
    'en-us': 'N/A',
    'ru-ru': 'Н/Д',
    'es-es': 'N/D',
    'fr-fr': 'N / A',
    'uk-ua': 'N/A',
    'de-ch': 'N/A',
  },
  new: {
    'en-us': 'New',
    'ru-ru': 'Новый',
    'es-es': 'Nuevo',
    'fr-fr': 'Nouveau',
    'uk-ua': 'новий',
    'de-ch': 'Neu',
  },
  edit: {
    'en-us': 'Edit',
    'ru-ru': 'Редактировать',
    'es-es': 'Editar',
    'fr-fr': 'Modifier',
    'uk-ua': 'Редагувати',
    'de-ch': 'Bearbeiten',
  },
  ignore: {
    'en-us': 'Ignore',
    'ru-ru': 'Игнорировать',
    'es-es': 'Ignorar',
    'fr-fr': 'Ignorer',
    'uk-ua': 'Ігнорувати',
    'de-ch': 'Ignorieren',
  },
  proceed: {
    'en-us': 'Proceed',
    'ru-ru': 'Продолжить',
    'es-es': 'Proceder',
    'fr-fr': 'Poursuivre',
    'uk-ua': 'Продовжуйте',
    'de-ch': 'Fortfahren',
  },
  start: {
    comment: 'Noun',
    'en-us': 'Start',
    'ru-ru': 'Начало',
    'es-es': 'Empezar',
    'fr-fr': 'Début',
    'uk-ua': 'старт',
    'de-ch': 'Start',
  },
  end: {
    comment: 'Noun',
    'en-us': 'End',
    'ru-ru': 'Конец',
    'es-es': 'Fin',
    'fr-fr': 'Fin',
    'uk-ua': 'Кінець',
    'de-ch': 'Ende',
  },
  update: {
    comment: 'Verb',
    'en-us': 'Update',
    'ru-ru': 'Обновлять',
    'es-es': 'Actualizar',
    'fr-fr': 'Mise à jour',
    'uk-ua': 'оновлення',
    'de-ch': 'Aktualisieren',
  },
  fullDate: {
    'en-us': 'Full Date',
    'es-es': 'Fecha completa',
    'de-ch': 'Vollständiges Datum',
    'fr-fr': 'Date complète',
    'ru-ru': 'Массовый выбор',
    'uk-ua': 'Розгорнути все',
  },
  view: {
    comment: 'Verb',
    'en-us': 'View',
    'ru-ru': 'Смотрет',
    'es-es': 'Ver',
    'fr-fr': 'Voir',
    'uk-ua': 'Переглянути',
    'de-ch': 'Ansicht',
  },
  opensInNewTab: {
    comment: 'Used in a hover-over message for links that open in new tab',
    'en-us': '(opens in a new tab)',
    'ru-ru': '(откроется в новой вкладке)',
    'es-es': '(se abre en una pestaña nueva)',
    'uk-ua': '(відкривається в новій вкладці)',
    'de-ch': '(Öffnet sich in einer neuen Registerkarte)',
    'fr-fr': "(s'ouvre dans un nouvel onglet)",
  },
  openInNewTab: {
    comment: 'Used in a button that opens a link in a new tab',
    'en-us': 'Open in New Tab',
    'ru-ru': 'Открыть в новой вкладке',
    'es-es': 'Abrir en una pestaña nueva',
    'fr-fr': 'Ouvrir dans un nouvel onglet',
    'uk-ua': 'Відкрити в новій вкладці',
    'de-ch': 'Öffnet sich in einer neuen Registerkarte',
  },
  goToHomepage: {
    'en-us': 'Go to Home Page',
    'ru-ru': 'Вернуться на домашнюю страницу',
    'es-es': 'Ir a la página de inicio',
    'fr-fr': "Aller à la page d'accueil",
    'uk-ua': 'Перейдіть на домашню сторінку',
    'de-ch': 'Zur Startseite gehen',
  },
  actions: {
    'en-us': 'Actions',
    'ru-ru': 'Действия',
    'es-es': 'Comportamientos',
    'fr-fr': 'Actions',
    'uk-ua': 'Дії',
    'de-ch': 'Aktionen',
  },
  chooseCollection: {
    'en-us': 'Choose Collection',
    'ru-ru': 'Выбрать коллекцию',
    'es-es': 'Elegir Colección',
    'fr-fr': 'Choisir une collection',
    'uk-ua': 'Виберіть колекцію',
    'de-ch': 'Sammlung auswählen',
  },
  ascending: {
    comment: 'As in "Ascending sort"',
    'en-us': 'Ascending',
    'ru-ru': 'Восходящий',
    'es-es': 'Ascendente',
    'fr-fr': 'Ascendant',
    'uk-ua': 'Висхідний',
    'de-ch': 'Aufsteigend',
  },
  descending: {
    comment: 'As in "Descending sort"',
    'en-us': 'Descending',
    'ru-ru': 'По убыванию',
    'es-es': 'Descendente',
    'fr-fr': 'Descendant',
    'uk-ua': 'Спускається',
    'de-ch': 'Absteigend',
  },
  recordSets: {
    'en-us': 'Record Sets',
    'ru-ru': 'Наборы записей',
    'es-es': 'Conjuntos de registros',
    'fr-fr': 'Enregistrements',
    'uk-ua': 'Набори рекордів',
    'de-ch': 'Satzgruppen',
  },
  recordCount: {
    'en-us': 'Record Count',
    'ru-ru': 'Количество записей',
    'es-es': 'Número de registros',
    'fr-fr': "Nombre d'enregistrements",
    'uk-ua': 'Підрахунок записів',
    'de-ch': 'Anzahl der Datensätze',
  },
  size: {
    'en-us': 'Size',
    'ru-ru': 'Размер',
    'es-es': 'Tamaño',
    'fr-fr': 'Taille',
    'uk-ua': 'Розмір',
    'de-ch': 'Grösse',
  },
  running: {
    'en-us': 'Running…',
    'ru-ru': 'Выполнение…',
    'es-es': 'Ejecutando…',
    'fr-fr': "En cours d'exécution…",
    'uk-ua': 'Виконується…',
    'de-ch': 'In Arbeit …',
  },
  noMatches: {
    'en-us': 'No Matches',
    'ru-ru': '(список сокращен)',
    'es-es': 'No hay coincidencias',
    'fr-fr': 'Pas de correspondance',
    'uk-ua': 'Немає збігів',
    'de-ch': 'Keine Treffer',
  },
  searchQuery: {
    'en-us': 'Search Query',
    'ru-ru': 'Поисковый запрос',
    'es-es': 'Consulta de busqueda',
    'fr-fr': 'Requête de recherche',
    'uk-ua': 'Пошуковий запит',
    'de-ch': 'Suchabfrage',
  },
  unknown: {
    'en-us': 'Unknown',
    'ru-ru': 'Неизвестный',
    'es-es': 'Desconocido',
    'fr-fr': 'Inconnu',
    'uk-ua': 'Невідомий',
    'de-ch': 'Unbekannt',
  },
  language: {
    'en-us': 'Language',
    'ru-ru': 'Язык',
    'es-es': 'Idioma',
    'fr-fr': 'Langue',
    'uk-ua': 'Мова',
    'de-ch': 'Sprache',
  },
  country: {
    'en-us': 'Country',
    'ru-ru': 'Страна',
    'es-es': 'País',
    'fr-fr': 'Pays',
    'uk-ua': 'Країна',
    'de-ch': 'Land',
  },
  viewRecord: {
    'en-us': 'View Record',
    'ru-ru': 'Посмотреть запись',
    'es-es': 'Ver registro',
    'fr-fr': "Afficher l'enregistrement",
    'uk-ua': 'Країна',
    'de-ch': 'Datensatz anzeigen',
  },
  nullInline: {
    'en-us': '(null)',
    'ru-ru': '(нулевой)',
    'es-es': '(nulo)',
    'fr-fr': '(null)',
    'uk-ua': '(нуль)',
    'de-ch': '(null)',
  },
  filePickerMessage: {
    comment: 'Generic. Could refer to any file',
    'en-us': 'Choose a file or drag it here',
    'ru-ru': 'Выберите файл или перетащите его сюда',
    'es-es': 'Elija un archivo o arrástrelo aquí',
    'fr-fr': 'Choisissez un fichier ou faites-le glisser ici',
    'uk-ua': 'Виберіть файл або перетягніть його сюди',
    'de-ch': 'Wählen eine Datei oder ziehen sie hierhin',
  },
  selectedFileName: {
    'en-us': 'Selected file',
    'ru-ru': 'Выбранный файл',
    'es-es': 'Fichero seleccionado',
    'fr-fr': 'Fichier sélectionné',
    'uk-ua': 'Вибраний файл',
    'de-ch': 'Gewählte Datei',
  },
  all: {
    'en-us': 'All',
    'ru-ru': 'Все',
    'es-es': 'Todo',
    'fr-fr': 'Tous',
    'uk-ua': 'всі',
    'de-ch': 'Alle',
  },
  unused: {
    'en-us': 'Unused',
    'ru-ru': 'Неиспользованный',
    'es-es': 'Sin usar',
    'fr-fr': 'Inutilisé',
    'uk-ua': 'Невикористаний',
    'de-ch': 'Unbenutzt',
  },
  ordinal: {
    'en-us': 'Ordinal',
    'ru-ru': 'Порядковый номер',
    'es-es': 'Ordinal',
    'fr-fr': 'Ordinal',
    'uk-ua': 'Порядковий',
    'de-ch': 'Reihenfolge',
  },
  export: {
    'en-us': 'Export',
    'ru-ru': 'Экспорт',
    'es-es': 'Exportar',
    'fr-fr': 'Exporter',
    'uk-ua': 'Експорт',
    'de-ch': 'Export',
  },
  import: {
    'en-us': 'Import',
    'ru-ru': 'Импортировать',
    'es-es': 'Importar',
    'fr-fr': 'Importer',
    'uk-ua': 'Масове вирішення',
    'de-ch': 'Import',
  },
  dismiss: {
    'en-us': 'Dismiss',
    'ru-ru': 'Отклонить',
    'es-es': 'Descartar',
    'fr-fr': 'Rejeter',
    'uk-ua': 'Відхилити',
    'de-ch': 'Ablehnen',
  },
  id: {
    'en-us': 'ID',
    'ru-ru': 'ID',
    'es-es': 'ID',
    'fr-fr': 'IDENTIFIANT',
    'uk-ua': 'ID',
    'de-ch': 'ID',
  },
  filter: {
    'en-us': 'Filter',
    'ru-ru': 'Фильтр',
    'es-es': 'Filtrar',
    'fr-fr': 'Filtre',
    'uk-ua': 'фільтр',
    'de-ch': 'Filter',
  },
  results: {
    'en-us': 'Results',
    'ru-ru': 'Полученные результаты',
    'es-es': 'Resultados',
    'fr-fr': 'Résultats',
    'uk-ua': 'Результати',
    'de-ch': 'Resultate',
  },
  downloadErrorMessage: {
    'en-us': 'Download Error Message',
    'ru-ru': 'Загрузить сообщение об ошибке',
    'es-es': 'Mensaje de error de descarga',
    'fr-fr': "Télécharger le message d'erreur",
    'uk-ua': 'Завантажити повідомлення про помилку',
    'de-ch': 'Fehlermeldung herunterladen',
  },
  copied: {
    'en-us': 'Copied!',
    'ru-ru': 'Скопировано!',
    'es-es': '¡Copiado!',
    'fr-fr': 'Copié !',
    'uk-ua': 'Скопійовано!',
    'de-ch': 'Wurde kopiert!',
  },
  copyToClipboard: {
    'en-us': 'Copy to clipboard',
    'ru-ru': 'Скопировать в буфер обмена',
    'es-es': 'Copiar al portapapeles',
    'fr-fr': 'Copier dans le presse-papier',
    'uk-ua': 'Копіювати в буфер обміну',
    'de-ch': 'In Zwischenablage kopieren',
  },
  selected: {
    'en-us': 'Selected',
    'ru-ru': 'Выбрано',
    'es-es': 'Seleccionado',
    'fr-fr': 'Sélectionné',
    'uk-ua': 'Вибране',
    'de-ch': 'Ausgewählt',
  },
  expand: {
    'en-us': 'Expand',
    'ru-ru': 'Расширять',
    'es-es': 'Desplegar',
    'fr-fr': 'Développer',
    'uk-ua': 'Розгорнути',
    'de-ch': 'Aufklappen',
  },
  expandAll: {
    'en-us': 'Expand All',
    'ru-ru': 'Расширить все',
    'es-es': 'Desplegar todo',
    'fr-fr': 'Développer tout',
    'uk-ua': 'Розгорнути все',
    'de-ch': 'Alle aufklappen',
  },
  collapse: {
    'en-us': 'Collapse',
    'es-es': 'Contraer',
    'fr-fr': 'Réduire',
    'ru-ru': 'Крах',
    'uk-ua': 'Згорнути',
    'de-ch': 'Zuklappen',
  },
  collapseAll: {
    'en-us': 'Collapse All',
    'ru-ru': 'Свернуть все',
    'es-es': 'Contraer todo',
    'fr-fr': 'Réduire tout',
    'uk-ua': 'Закрити все',
    'de-ch': 'Alle zuklappen',
  },
  reset: {
    'en-us': 'Reset',
    'ru-ru': 'Перезагрузить',
    'es-es': 'Reiniciar',
    'fr-fr': 'Réinitialiser',
    'uk-ua': 'Скинути',
    'de-ch': 'Zurücksetzen',
  },
  select: {
    'en-us': 'Select',
    'ru-ru': 'Нет совпадений',
    'es-es': 'Seleccionar',
    'fr-fr': 'Sélectionner',
    'uk-ua': 'Виберіть',
    'de-ch': 'Auswählen',
  },
  none: {
    'en-us': 'None',
    'ru-ru': 'Никто',
    'es-es': 'Ninguno',
    'fr-fr': 'Aucun',
    'uk-ua': 'Жодного',
    'de-ch': 'Keine',
  },
  noneAvailable: {
    'en-us': 'None available',
    'ru-ru': 'Нет доступных',
    'es-es': 'Ninguno disponible',
    'fr-fr': 'Aucun disponible',
    'uk-ua': 'Немає доступних',
    'de-ch': 'Keine Verfügbar',
  },
  countLine: {
    comment: 'Example usage: Record Sets (1,234)',
    'en-us': '{resource:string} ({count:number|formatted})',
    'ru-ru': '{resource:string} ({count:number|formatted})',
    'es-es': '{resource:string} ({count:number|formatted})',
    'fr-fr': '{resource:string} ({count:number|formatted})',
    'uk-ua': '{resource:string} ({count:number|formatted})',
    'de-ch': '{resource:string} ({count:number|formatted})',
  },
  jsxCountLine: {
    comment: 'Example usage: Record Sets (1,234)',
    'en-us': '{resource:string} <wrap>({count:number|formatted})</wrap>',
    'ru-ru': '{resource:string} <wrap>({count:number|formatted})</wrap>',
    'es-es': '{resource:string} <wrap>({count:number|formatted})</wrap>',
    'fr-fr': '{resource:string} <wrap>({count:number|formatted})</wrap>',
    'uk-ua': '{resource:string} <wrap>({count:number|formatted})</wrap>',
    'de-ch': '{resource:string} <wrap>({count:number|formatted})</wrap>',
  },
  colonHeader: {
    comment: `
      Example usage: "Choose collection:". Used only if there is nothing else on
      this line after the colon heading
    `,
    'en-us': '{header:string}:',
    'ru-ru': '{header:string}:',
    'es-es': '{header:string}:',
    'fr-fr': '{header:string} :',
    'uk-ua': '{header:string}:',
    'de-ch': '{header:string}:',
  },
  colonLine: {
    comment: `
      Example usage: "Created by: Full Name" OR "Record Set: Record Set Name"
    `,
    'en-us': '{label:string}: {value:string}',
    'ru-ru': '{label:string}: {value:string}',
    'es-es': '{label:string}: {value:string}',
    'fr-fr': '{label:string} : {value:string}',
    'uk-ua': '{label:string}: {value:string}',
    'de-ch': '{label:string}: {value:string}',
  },
  jsxColonLine: {
    comment: `
      Example usage: "Created by: Full Name" OR "Record Set: Record Set Name"
    `,
    'en-us': '{label:string}: <wrap />',
    'ru-ru': '{label:string}: <wrap />',
    'es-es': '{label:string}: <wrap />',
    'fr-fr': '{label:string} : <wrap />',
    'uk-ua': '{label:string}: <wrap />',
    'de-ch': '{label:string}: <wrap />',
  },
  bulkSelect: {
    'en-us': 'Bulk Select',
    'es-es': 'Selección masiva',
    'de-ch': 'Mehrfachauswahl',
    'fr-fr': 'Voir',
    'ru-ru': 'Массовый выбор',
    'uk-ua': 'Завантаження…',
  },
  bulkReturn: {
    'en-us': 'Bulk Return',
    'de-ch': 'Massenrücksendung',
    'es-es': 'Devolución masiva',
    'fr-fr': 'Retour groupé',
    'ru-ru': 'Массовый возврат',
    'uk-ua': 'Масове повернення',
  },
  bulkResolve: {
    'en-us': 'Bulk Resolve',
    'de-ch': 'Massenauflösung',
    'es-es': 'Resolución masiva',
    'fr-fr': 'Résolution groupée',
    'ru-ru': 'Массовое решение',
    'uk-ua': 'Масове вирішення',
  },
  timeRemaining: {
    'en-us': 'Time remaining',
    'es-es': 'Tiempo restante',
    'fr-fr': 'Temps restant',
    'ru-ru': 'Времени осталось',
    'uk-ua': 'Час, що залишився',
    'de-ch': 'Noch verbleibende Zeit',
  },
  unlimited: {
    'en-us': 'Unlimited',
    'de-ch': 'Unbegrenzt',
    'es-es': 'Ilimitado',
    'fr-fr': 'Illimité',
    'ru-ru': 'Безлимитный',
    'uk-ua': 'Необмежений',
  },
  change: {
    comment: 'Verb',
    'en-us': 'Change',
    'de-ch': 'Ändern',
    'es-es': 'Cambiar',
    'fr-fr': 'Changement',
    'ru-ru': 'Изменять',
    'uk-ua': 'Зміна',
  },
  dontShowAgain: {
    'en-us': "Don't show this again",
    'es-es': 'No volver a mostrar esto',
    'fr-fr': 'Ne montre plus à nouveau',
    'ru-ru': 'Больше не показывать это',
    'uk-ua': 'Не показувати це знову',
    'de-ch': 'Wählen Sie Dateien aus oder ziehen Sie sie hierher',
  },
  multipleFilePickerMessage: {
    'en-us': 'Choose files or drag them here',
    'de-ch': 'Wählen Sie Dateien aus oder ziehen Sie sie hierher',
    'es-es': 'Seleccione los archivos o arrástrelos hasta aquí',
    'fr-fr': 'Choisissez des fichiers ou faites-les glisser ici',
    'ru-ru': 'Выберите файлы или перетащите их сюда',
    'uk-ua': 'Виберіть файли або перетягніть їх сюди',
  },
} as const);
