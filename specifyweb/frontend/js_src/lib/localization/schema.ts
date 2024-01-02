/**
 * Localization strings used in the Schema Config and data model viewer
 *
 * @module
 */

import { createDictionary } from './utils';

// Refer to "Guidelines for Programmers" in ./README.md before editing this file

export const schemaText = createDictionary({
  table: {
    'en-us': 'Table',
    'ru-ru': 'Стол',
    'es-es': 'Tabla',
    'fr-fr': 'Tableau',
    'uk-ua': 'Таблиця',
    'de-ch': 'Tabelle',
  },
  tables: {
    'en-us': 'Tables',
    'ru-ru': 'Таблицы',
    'es-es': 'Tablas',
    'fr-fr': 'Tableaux',
    'uk-ua': 'Таблиці',
    'de-ch': 'Tabellen',
  },
  tableName: {
    'en-us': 'Table Name',
    'ru-ru': 'Имя таблицы',
    'es-es': 'Relaciones',
    'fr-fr': 'Nom du tableau',
    'uk-ua': 'Назва таблиці',
    'de-ch': 'Tabellennamen',
  },
  schemaConfig: {
    'en-us': 'Schema Config',
    'ru-ru': 'Конфигурация схемы',
    'es-es': 'Configuración de esquema',
    'fr-fr': 'Configuration du schéma',
    'uk-ua': 'Конфігурація схеми бази даних',
    'de-ch': 'Schema konfigurieren',
  },
  unsavedSchemaUnloadProtect: {
    'en-us': 'Schema changes have not been saved',
    'ru-ru': 'Изменения схемы не сохранены.',
    'es-es': 'Los cambios de esquema no se han guardado.',
    'fr-fr': "Les modifications du schéma n'ont pas été enregistrées",
    'uk-ua': 'Зміни схеми не збережено',
    'de-ch': 'Schema Änderungen wurden nicht gespeichert',
  },
  changeBaseTable: {
    'en-us': 'Change Base Table',
    'ru-ru': 'Изменить базовую таблицу',
    'es-es': 'Cambiar tabla base',
    'fr-fr': 'Modifier la base de tableau',
    'uk-ua': 'Змінити базову таблицю',
    'de-ch': 'Basis-Tabelle ändern',
  },
  field: {
    'en-us': 'Field',
    'ru-ru': 'Поле',
    'es-es': 'Campo',
    'fr-fr': 'Champ',
    'uk-ua': 'Поле',
    'de-ch': 'Feld',
  },
  fields: {
    'en-us': 'Fields',
    'ru-ru': 'Поля',
    'es-es': 'Campos',
    'fr-fr': 'Champs',
    'uk-ua': 'Поля',
    'de-ch': 'Felder',
  },
  relationships: {
    'en-us': 'Relationships',
    'ru-ru': 'Отношения',
    'es-es': 'Relaciones',
    'fr-fr': 'Relations',
    'uk-ua': 'Стосунки',
    'de-ch': 'Beziehungen',
  },
  database: {
    'en-us': 'Database',
  },
  setScope: {
    'en-us': 'Set Scope',
  },
  caption: {
    'en-us': 'Caption',
    'ru-ru': 'Подпись',
    'es-es': 'Subtítulo',
    'fr-fr': 'Légende',
    'uk-ua': 'Підпис',
    'de-ch': 'Beschriftung',
  },
  description: {
    'en-us': 'Description',
    'ru-ru': 'Описание',
    'es-es': 'Descripción',
    'fr-fr': 'Description',
    'uk-ua': 'Опис',
    'de-ch': 'Beschreibung',
  },
  hideTable: {
    'en-us': 'Hide Table',
    'ru-ru': 'Скрыть таблицу',
    'es-es': 'Ocultar tabla',
    'fr-fr': 'Masquer le tableau',
    'uk-ua': 'Приховати таблицю',
    'de-ch': 'Tabelle verbergen',
  },
  hideField: {
    'en-us': 'Hide Field',
    'ru-ru': 'Скрыть поле',
    'es-es': 'Ocultar campo',
    'fr-fr': 'Masquer le champ',
    'uk-ua': 'Приховати поле',
    'de-ch': 'Feld verbergen',
  },
  tableFormat: {
    'en-us': 'Table Format',
    'ru-ru': 'Формат таблицы',
    'es-es': 'Formato de tabla',
    'fr-fr': 'Format de tableau',
    'uk-ua': 'Формат таблиці',
    'de-ch': 'Tabellenformat',
  },
  tableAggregation: {
    'en-us': 'Table Aggregation',
    'ru-ru': 'Агрегация таблиц',
    'es-es': 'Agregación de tablas',
    'fr-fr': 'Agrégation de tableaux',
    'uk-ua': 'Агрегація таблиць',
    'de-ch': 'Tabellenaggregation',
  },
  oneToOne: {
    'en-us': 'One-to-one',
    'ru-ru': 'Один к одному',
    'es-es': 'Cara a cara',
    'fr-fr': 'Un à un',
    'uk-ua': 'Один до один',
    'de-ch': 'Eins zu eins',
  },
  oneToMany: {
    'en-us': 'One-to-many',
    'ru-ru': 'Один ко многим',
    'es-es': 'Uno a muchos',
    'fr-fr': 'Un à plusieurs',
    'uk-ua': 'Один до багатьох',
    'de-ch': 'Eins zu vielen',
  },
  manyToOne: {
    'en-us': 'Many-to-one',
    'ru-ru': 'Многие к одному',
    'es-es': 'muchos a uno',
    'fr-fr': 'Plusieurs à un',
    'uk-ua': 'Багато-до-одного',
    'de-ch': 'Viele zu eins',
  },
  manyToMany: {
    'en-us': 'many-to-many',
    'ru-ru': 'многие-ко-многим',
    'es-es': 'muchos a muchos',
    'fr-fr': 'Plusieurs à plusieurs',
    'uk-ua': 'багато-до-багатьох',
    'de-ch': 'Viele zu viele',
  },
  fieldLength: {
    'en-us': 'Length',
    'ru-ru': 'Длина',
    'es-es': 'Longitud',
    'fr-fr': 'Longueur',
    'uk-ua': 'Довжина',
    'de-ch': 'Länge',
  },
  readOnly: {
    'en-us': 'Read-only',
    'ru-ru': 'Только чтение',
    'es-es': 'Solo lectura',
    'fr-fr': 'Lecture seule',
    'uk-ua': 'Лише для читання',
    'de-ch': 'Nur-Lesen',
  },
  fieldFormat: {
    'en-us': 'Field Format',
    'ru-ru': 'Формат поля',
    'es-es': 'Formato de campo',
    'fr-fr': 'Format de champ',
    'uk-ua': 'Формат поля',
    'de-ch': 'Feldformat',
  },
  formatted: {
    'en-us': 'Formatted',
    'ru-ru': 'Отформатированный',
    'es-es': 'formateado',
    'fr-fr': 'Formaté',
    'uk-ua': 'Відформатований',
    'de-ch': 'Formatiert',
  },
  webLink: {
    'en-us': 'Web Link',
    'ru-ru': 'Интернет-ссылка',
    'es-es': 'Enlace web',
    'fr-fr': 'Lien Web',
    'uk-ua': 'Веб посилання',
    'de-ch': 'Web-Link',
  },
  userDefined: {
    'en-us': 'User Defined',
    'ru-ru': 'Один к одному',
    'es-es': 'Cara a cara',
    'fr-fr': "Défini par l'utilisateur",
    'uk-ua': 'Визначений користувачем',
    'de-ch': 'Benutzerdefiniert',
  },
  addLanguage: {
    'en-us': 'Add Language',
    'ru-ru': 'Количество отношений',
    'es-es': 'recuento de relaciones',
    'fr-fr': 'Ajouter une langue',
    'uk-ua': 'Додати мову',
    'de-ch': 'Sprache hinzuzufügen',
  },
  fieldLabel: {
    'en-us': 'Label',
    'ru-ru': 'Этикетка',
    'es-es': 'Longitud',
    'fr-fr': 'Étiquette',
    'uk-ua': 'Підпис',
    'de-ch': 'Etikett',
  },
  databaseColumn: {
    'en-us': 'Database Column',
    'ru-ru': 'Столбец базы данных',
    'es-es': 'Columna de base de datos',
    'fr-fr': 'Colonne de base de données',
    'uk-ua': 'Стовпець бази даних',
    'de-ch': 'Datenbank-Spalte',
  },
  relatedModel: {
    'en-us': 'Related Model',
    'ru-ru': 'Сопутствующая модель',
    'es-es': 'Modelo relacionado',
    'fr-fr': 'Modèle associé',
    'uk-ua': "Пов'язана модель",
    'de-ch': 'Zugehöriges Modell',
  },
  otherSideName: {
    'en-us': 'Other side name',
    'ru-ru': 'Длина',
    'es-es': 'Longitud',
    'fr-fr': "Nom de l'autre côté",
    'uk-ua': "Ім'я на іншій стороні",
    'de-ch': 'Name der anderen Seite',
  },
  dependent: {
    'en-us': 'Dependent',
    'ru-ru': 'Зависимый',
    'es-es': 'Dependiente',
    'fr-fr': 'Dépendant',
    'uk-ua': 'Залежний',
    'de-ch': 'Abhängig',
  },
  independent: {
    'en-us': 'Independent',
    'es-es': 'Independiente',
    'fr-fr': 'Indépendant',
    'ru-ru': 'Независимый',
    'uk-ua': 'Незалежний',
    'de-ch': 'Unabhängig',
  },
  downloadAsJson: {
    'en-us': 'Download as JSON',
    'ru-ru': 'Скачать в формате JSON',
    'es-es': 'Descargar como JSON',
    'fr-fr': 'Télécharger au format JSON',
    'uk-ua': 'Завантажити як JSON',
    'de-ch': 'Als JSON herunterladen',
  },
  downloadAsXml: {
    'en-us': 'Download as XML',
    'ru-ru': 'Скачать как XML',
    'es-es': 'Descargar como XML',
    'fr-fr': 'Télécharger au format XML',
    'uk-ua': 'Завантажити як XML',
    'de-ch': 'Als XML herunterladen',
  },
  downloadAsTsv: {
    'en-us': 'Download as TSV',
    'ru-ru': 'Скачать как TSV',
    'es-es': 'Descargar como TSV',
    'fr-fr': 'Télécharger au format TSV',
    'uk-ua': 'Завантажити як TSV',
    'de-ch': 'Als TSV herunterladen',
  },
  tableId: {
    'en-us': 'Table ID',
    'ru-ru': 'Идентификатор таблицы',
    'es-es': 'ID de tabla',
    'fr-fr': 'ID du tableau',
    'uk-ua': 'Ідентифікатор таблиці',
    'de-ch': 'Tabellen-ID',
  },
  fieldCount: {
    'en-us': 'Field count',
    'ru-ru': 'Количество полей',
    'es-es': 'Recuento de campos',
    'fr-fr': 'Nombre de champs',
    'uk-ua': 'Кількість полів',
    'de-ch': 'Anzahl Felder',
  },
  relationshipCount: {
    'en-us': 'Relationship count',
    'ru-ru': 'Количество отношений',
    'es-es': 'recuento de relaciones',
    'fr-fr': 'Nombre de relations',
    'uk-ua': 'Кількість стосунків',
    'de-ch': 'Anzahl Beziehungen',
  },
  databaseSchema: {
    'en-us': 'Database Schema',
    'ru-ru': 'Схема базы данных',
    'es-es': 'Esquema de base de datos',
    'fr-fr': 'Schéma de base de données',
    'uk-ua': 'Схема бази даних',
    'de-ch': 'Datenbankschema',
  },
  selectedTables: {
    'en-us': 'Selected Tables',
    'ru-ru': 'Выбранные таблицы',
    'es-es': 'Tablas seleccionadas',
    'fr-fr': 'Tableaux sélectionnés',
    'uk-ua': 'Вибрані таблиці',
    'de-ch': 'Ausgewählte Tabellen',
  },
  possibleTables: {
    'en-us': 'Possible Tables',
    'ru-ru': 'Возможные таблицы',
    'es-es': 'Posibles tablas',
    'fr-fr': 'Tableaux possibles',
    'uk-ua': 'Можливі таблиці',
    'de-ch': 'Mögliche Tabellen',
  },
  goToTop: {
    'en-us': 'Go to top',
    'es-es': 'Ve arriba',
    'fr-fr': 'Aller en haut',
    'ru-ru': 'Перейти наверх',
    'uk-ua': 'Перейти вгору',
    'de-ch': 'Nach oben',
  },
  idField: {
    'en-us': 'ID Field',
    'es-es': 'Campo de identificación',
    'fr-fr': "Champ d'identification",
    'ru-ru': 'Поле идентификатора',
    'uk-ua': 'ID Поле',
    'de-ch': 'Feld-ID',
  },
  uniquenessRules: {
    'en-us': 'Uniqueness Rules',
  },
  uniqueFields: {
    'en-us': 'Unique Fields',
  },
  addUniquenessRule: {
    'en-us': 'Add Uniqueness Rule',
  },
  configureUniquenessRule: {
    'en-us': 'Configure Uniqueness Rule',
  },
  scope: {
    'en-us': 'Scope',
    'es-es': 'Alcance',
    'fr-fr': 'Configuration du schéma : [X15X]',
    'ru-ru': 'Объем',
    'uk-ua': 'Область застосування',
    'de-ch': 'Anwendungsbereich',
  },
  exportDuplicates: {
    'en-us': 'Export Duplicates',
  },
  schemaViewTitle: {
    'en-us': 'Schema Config: {tableName:string}',
    'es-es': 'Configuración de esquema: {tableName:string}',
    'fr-fr': 'Configuration du schéma : {tableName :string}',
    'ru-ru': 'Конфигурация схемы: {tableName:string}',
    'uk-ua': 'Конфігурація схеми: {tableName:string}',
    'de-ch': 'Schema-Konfiguration: {tableName:string}',
  },
  schemaExportFileName: {
    'en-us': 'Specify 7 Data Model',
    'ru-ru': 'Укажите 7 моделей данных',
    'es-es': 'Especifique 7 modelos de datos',
    'fr-fr': 'Specify 7 Modèle de données',
    'uk-ua': 'Specify 7 Модель даних',
    'de-ch': 'Specify 7 Datenmodell',
  },
} as const);
