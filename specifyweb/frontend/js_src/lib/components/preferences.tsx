/**
 * Definitions for User Interface preferences (scoped to a SpecifyUser)
 */

import React from 'react';

import type { Collection } from '../datamodel';
import { commonText } from '../localization/common';
import { formsText } from '../localization/forms';
import { preferencesText } from '../localization/preferences';
import { queryText } from '../localization/query';
import type { Language } from '../localization/utils';
import { DEFAULT_LANGUAGE } from '../localization/utils';
import { wbText } from '../localization/workbench';
import type { JavaType } from '../specifyfield';
import type { IR, RA } from '../types';
import { ensure } from '../types';
import type { Parser } from '../uiparse';
import { Link } from './basic';
import { crash } from './errorboundary';
import type { WelcomePageMode } from './preferencesrenderers';
import {
  CollectionSortOrderPreferenceItem,
  ColorPickerPreferenceItem,
  defaultFont,
  defaultWelcomePageImage,
  FontFamilyPreferenceItem,
  WelcomePageModePreferenceItem,
} from './preferencesrenderers';
import {
  handleLanguageChange,
  LanguagePreferencesItem,
  SchemaLanguagePreferenceItem,
} from './toolbar/language';

// Custom Renderer for a preference item
export type PreferenceItemComponent<VALUE> = (props: {
  readonly definition: PreferenceItem<VALUE>;
  readonly value: VALUE;
  readonly onChange: (value: VALUE) => void;
  readonly isReadOnly: boolean;
}) => JSX.Element;

export type PreferenceItem<VALUE> = {
  readonly title: string | JSX.Element;
  readonly description?: string | JSX.Element;
  // Whether app needs to be reloaded if this preference changes
  readonly requiresReload: boolean;
  /*
   * Whether to render this item in the Preferences Menu
   * Invisible items are usually set by components outside the preferences menu
   *
   * If 'adminsOnly' then visible only to admin users
   */
  readonly visible: boolean | 'adminsOnly';
  readonly defaultValue: VALUE;
  // Custom onChange handler
  readonly onChange?: (value: VALUE) => void | Promise<void>;
} & (
  | {
      readonly values:
        | RA<VALUE>
        | RA<{
            readonly value: VALUE;
            readonly title?: string;
            readonly description?: string;
          }>;
    }
  | {
      // Parses the stored value. Determines the input type to render
      readonly type: JavaType;
      readonly parser?: Parser;
    }
  | {
      readonly renderer: PreferenceItemComponent<VALUE>;
    }
);

/**
 * This is used to enforce the same generic value be used inside a PreferenceItem
 */
const defineItem = <VALUE,>(
  definition: PreferenceItem<VALUE>
): PreferenceItem<VALUE> => definition;

export type GenericPreferencesCategories = IR<{
  readonly title: string;
  readonly description?: string;
  readonly subCategories: IR<{
    readonly title: string;
    readonly description?: string;
    readonly items: IR<PreferenceItem<any>>;
  }>;
}>;
// TODO: reduce amount of items that have requiresReload=true
export const preferenceDefinitions = {
  general: {
    title: preferencesText('general'),
    subCategories: {
      ui: {
        title: preferencesText('ui'),
        items: {
          language: defineItem<Language>({
            title: preferencesText('language'),
            requiresReload: true,
            visible: true,
            defaultValue: DEFAULT_LANGUAGE,
            onChange: handleLanguageChange,
            renderer: LanguagePreferencesItem,
          }),
          theme: defineItem<'system' | 'light' | 'dark'>({
            title: preferencesText('theme'),
            requiresReload: false,
            visible: true,
            defaultValue: 'system',
            values: [
              {
                value: 'system',
                title: preferencesText('system'),
                description: preferencesText('inheritOsSettings'),
              },
              {
                value: 'light',
                title: preferencesText('light'),
              },
              {
                value: 'dark',
                title: preferencesText('dark'),
              },
            ],
          }),
          reduceMotion: defineItem<'system' | 'reduce' | 'noPreference'>({
            title: preferencesText('reduceMotion'),
            description: preferencesText('reduceMotionDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: 'system',
            values: [
              {
                value: 'system',
                title: preferencesText('system'),
                description: preferencesText('inheritOsSettings'),
              },
              {
                value: 'reduce',
                title: preferencesText('reduce'),
              },
              {
                value: 'noPreference',
                title: preferencesText('noPreference'),
              },
            ],
          }),
          reduceTransparency: defineItem<'system' | 'reduce' | 'noPreference'>({
            title: preferencesText('reduceTransparency'),
            description: preferencesText('reduceTransparencyDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: 'system',
            values: [
              {
                value: 'system',
                title: preferencesText('system'),
                description: preferencesText('inheritOsSettings'),
              },
              {
                value: 'reduce',
                title: preferencesText('reduce'),
              },
              {
                value: 'noPreference',
                title: preferencesText('noPreference'),
              },
            ],
          }),
          fontSize: defineItem<number>({
            title: preferencesText('fontSize'),
            requiresReload: false,
            visible: true,
            defaultValue: 100,
            type: 'java.lang.Double',
            parser: {
              min: 1,
              max: 1000,
            },
          }),
          scaleInterface: defineItem<boolean>({
            title: preferencesText('scaleInterface'),
            description: preferencesText('scaleInterfaceDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          fontFamily: defineItem<string>({
            title: preferencesText('fontFamily'),
            description: preferencesText('fontFamilyDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: defaultFont,
            renderer: FontFamilyPreferenceItem,
          }),
        },
      },
      appearance: {
        title: preferencesText('appearance'),
        items: {
          background: defineItem({
            title: preferencesText('background'),
            requiresReload: false,
            visible: true,
            defaultValue: '#ffffff',
            renderer: ColorPickerPreferenceItem,
          }),
          darkBackground: defineItem({
            title: preferencesText('darkBackground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#171717',
            renderer: ColorPickerPreferenceItem,
          }),
          accentColor1: defineItem({
            title: preferencesText('accentColor1'),
            requiresReload: false,
            visible: true,
            defaultValue: '#ffcda3',
            renderer: ColorPickerPreferenceItem,
          }),
          accentColor2: defineItem({
            title: preferencesText('accentColor2'),
            requiresReload: false,
            visible: true,
            defaultValue: '#ff9742',
            renderer: ColorPickerPreferenceItem,
          }),
          accentColor3: defineItem({
            title: preferencesText('accentColor3'),
            requiresReload: false,
            visible: true,
            defaultValue: '#ff811a',
            renderer: ColorPickerPreferenceItem,
          }),
          accentColor4: defineItem({
            title: preferencesText('accentColor4'),
            requiresReload: false,
            visible: true,
            defaultValue: '#d15e00',
            renderer: ColorPickerPreferenceItem,
          }),
          accentColor5: defineItem({
            title: preferencesText('accentColor5'),
            requiresReload: false,
            visible: true,
            defaultValue: '#703200',
            renderer: ColorPickerPreferenceItem,
          }),
        },
      },
      application: {
        title: preferencesText('application'),
        items: {
          allowDismissingErrors: defineItem<boolean>({
            title: preferencesText('allowDismissingErrors'),
            requiresReload: false,
            visible: 'adminsOnly',
            defaultValue: false,
            type: 'java.lang.Boolean',
          }),
        },
      },
      dialog: {
        title: preferencesText('dialogs'),
        items: {
          updatePageTitle: defineItem<boolean>({
            title: preferencesText('updatePageTitle'),
            description: preferencesText('updatePageTitleDialogDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          transparentBackground: defineItem<boolean>({
            title: preferencesText('translucentDialog'),
            description: preferencesText('translucentDialogDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: false,
            type: 'java.lang.Boolean',
          }),
          showIcon: defineItem<boolean>({
            title: preferencesText('showDialogIcon'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          closeOnEsc: defineItem<boolean>({
            title: preferencesText('closeOnEsc'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          closeOnOutsideClick: defineItem<boolean>({
            title: preferencesText('closeOnOutsideClick'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
        },
      },
    },
  },
  header: {
    title: preferencesText('header'),
    subCategories: {
      menu: {
        title: preferencesText('menu'),
        items: {
          showDataEntry: defineItem<boolean>({
            title: preferencesText('showDataEntry'),
            requiresReload: true,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          showInteractions: defineItem<boolean>({
            title: preferencesText('showInteractions'),
            requiresReload: true,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          showTrees: defineItem<boolean>({
            title: preferencesText('showTrees'),
            requiresReload: true,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          showRecordSets: defineItem<boolean>({
            title: preferencesText('showRecordSets'),
            requiresReload: true,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          showQueries: defineItem<boolean>({
            title: preferencesText('showQueries'),
            requiresReload: true,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          showReports: defineItem<boolean>({
            title: preferencesText('showReports'),
            requiresReload: true,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          showAttachments: defineItem<boolean>({
            title: preferencesText('showAttachments'),
            requiresReload: true,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          showWorkBench: defineItem<boolean>({
            title: preferencesText('showWorkBench'),
            requiresReload: true,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
        },
      },
    },
  },
  form: {
    title: commonText('forms'),
    subCategories: {
      schema: {
        title: commonText('schemaConfig'),
        items: {
          language: defineItem<string>({
            title: preferencesText('language'),
            requiresReload: true,
            visible: true,
            defaultValue: 'en',
            renderer: SchemaLanguagePreferenceItem,
          }),
        },
      },
      behavior: {
        title: preferencesText('behavior'),
        items: {
          autoNumbering: defineItem<boolean>({
            title: preferencesText('enableAutoNumbering'),
            description: preferencesText('enableAutoNumberingDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          textAreaAutoGrow: defineItem<boolean>({
            title: preferencesText('textAreaAutoGrow'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
        },
      },
      definition: {
        title: preferencesText('definition'),
        items: {
          flexibleColumnWidth: defineItem<boolean>({
            title: preferencesText('flexibleColumnWidth'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
        },
      },
      ui: {
        title: preferencesText('ui'),
        items: {
          updatePageTitle: defineItem<boolean>({
            title: preferencesText('updatePageTitle'),
            description: preferencesText('updatePageTitleFormDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          tableNameInTitle: defineItem<boolean>({
            title: preferencesText('tableNameInTitle'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          fontSize: defineItem<number>({
            title: preferencesText('fontSize'),
            requiresReload: false,
            visible: true,
            defaultValue: 100,
            type: 'java.lang.Float',
            parser: {
              min: 1,
              max: 1000,
            },
          }),
          fontFamily: defineItem<string>({
            title: preferencesText('fontFamily'),
            description: preferencesText('fontFamilyDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: defaultFont,
            renderer: FontFamilyPreferenceItem,
          }),
          maxWidth: defineItem<number>({
            title: preferencesText('maxWidth'),
            requiresReload: false,
            visible: true,
            defaultValue: 1200,
            type: 'java.lang.Float',
            parser: {
              min: 100,
              max: 10_000,
            },
          }),
          specifyNetworkBadge: defineItem<boolean>({
            title: preferencesText('specifyNetworkBadge'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          useAccessibleFullDatePicker: defineItem<boolean>({
            title: preferencesText('useAccessibleFullDatePicker'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          useAccessibleMonthPicker: defineItem<boolean>({
            title: preferencesText('useAccessibleMonthPicker'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
        },
      },
      fieldBackground: {
        title: preferencesText('fieldBackgrounds'),
        items: {
          default: defineItem({
            title: preferencesText('fieldBackground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#e5e7eb',
            renderer: ColorPickerPreferenceItem,
          }),
          disabled: defineItem({
            title: preferencesText('disabledFieldBackground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#ffffff',
            renderer: ColorPickerPreferenceItem,
          }),
          invalid: defineItem({
            title: preferencesText('invalidFieldBackground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#f87171',
            renderer: ColorPickerPreferenceItem,
          }),
          required: defineItem({
            title: preferencesText('requiredFieldBackground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#bfdbfe',
            renderer: ColorPickerPreferenceItem,
          }),
          darkDefault: defineItem({
            title: preferencesText('darkFieldBackground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#404040',
            renderer: ColorPickerPreferenceItem,
          }),
          darkDisabled: defineItem({
            title: preferencesText('darkDisabledFieldBackground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#171717',
            renderer: ColorPickerPreferenceItem,
          }),
          darkInvalid: defineItem({
            title: preferencesText('darkInvalidFieldBackground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#991b1b',
            renderer: ColorPickerPreferenceItem,
          }),
          darkRequired: defineItem({
            title: preferencesText('darkRequiredFieldBackground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#1e3a8a',
            renderer: ColorPickerPreferenceItem,
          }),
        },
      },
      appearance: {
        title: preferencesText('appearance'),
        items: {
          foreground: defineItem({
            title: preferencesText('foreground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#ffffff',
            renderer: ColorPickerPreferenceItem,
          }),
          background: defineItem({
            title: preferencesText('background'),
            requiresReload: false,
            visible: true,
            defaultValue: '#e5e7eb',
            renderer: ColorPickerPreferenceItem,
          }),
          darkForeground: defineItem({
            title: preferencesText('darkForeground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#171717',
            renderer: ColorPickerPreferenceItem,
          }),
          darkBackground: defineItem({
            title: preferencesText('darkBackground'),
            requiresReload: false,
            visible: true,
            defaultValue: '#262626',
            renderer: ColorPickerPreferenceItem,
          }),
        },
      },
      queryComboBox: {
        title: preferencesText('queryComboBox'),
        items: {
          searchAlgorithm: defineItem<
            'startsWith' | 'startsWithCaseSensitive' | 'contains'
          >({
            title: preferencesText('searchAlgorithm'),
            requiresReload: false,
            visible: true,
            defaultValue: 'startsWith',
            values: [
              {
                value: 'startsWith',
                title: preferencesText('startsWith'),
                description: preferencesText('startsWithDescription'),
              },
              {
                value: 'startsWithCaseSensitive',
                title: preferencesText('startsWithCaseSensitive'),
                description: preferencesText(
                  'startsWithCaseSensitiveDescription'
                ),
              },
              {
                value: 'contains',
                title: preferencesText('contains'),
                description: preferencesText('containsDescription'),
              },
            ],
          }),
          highlightMatch: defineItem<boolean>({
            title: preferencesText('highlightMatch'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          autoGrowAutoComplete: defineItem<boolean>({
            title: preferencesText('autoGrowAutoComplete'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          closeOnOutsideClick: defineItem<boolean>({
            title: preferencesText('closeOnOutsideClick'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
        },
      },
    },
  },
  chooseCollection: {
    title: commonText('chooseCollection'),
    subCategories: {
      general: {
        title: preferencesText('general'),
        items: {
          alwaysPrompt: defineItem<boolean>({
            title: preferencesText('alwaysPrompt'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          sortOrder: defineItem<
            keyof Collection['fields'] | `-${keyof Collection['fields']}`
          >({
            title: formsText('order'),
            requiresReload: false,
            visible: true,
            defaultValue: 'collectionName',
            renderer: CollectionSortOrderPreferenceItem,
          }),
        },
      },
    },
  },
  treeEditor: {
    title: preferencesText('treeEditor'),
    subCategories: {
      geography: {
        /*
         * This would be replaced with labels from schema once
         * schema is loaded
         */
        title: '_Geography',
        items: {
          treeAccentColor: defineItem({
            title: preferencesText('treeAccentColor'),
            requiresReload: false,
            visible: true,
            defaultValue: '#f79245',
            renderer: ColorPickerPreferenceItem,
          }),
          synonymColor: defineItem({
            title: preferencesText('synonymColor'),
            requiresReload: false,
            visible: true,
            defaultValue: '#dc2626',
            renderer: ColorPickerPreferenceItem,
          }),
        },
      },
      taxon: {
        title: '_Taxon',
        items: {
          treeAccentColor: defineItem({
            title: preferencesText('treeAccentColor'),
            requiresReload: false,
            visible: true,
            defaultValue: '#f79245',
            renderer: ColorPickerPreferenceItem,
          }),
          synonymColor: defineItem({
            title: preferencesText('synonymColor'),
            requiresReload: false,
            visible: true,
            defaultValue: '#dc2626',
            renderer: ColorPickerPreferenceItem,
          }),
        },
      },
      storage: {
        title: '_Storage',
        items: {
          treeAccentColor: defineItem({
            title: preferencesText('treeAccentColor'),
            requiresReload: false,
            visible: true,
            defaultValue: '#f79245',
            renderer: ColorPickerPreferenceItem,
          }),
          synonymColor: defineItem({
            title: preferencesText('synonymColor'),
            requiresReload: false,
            visible: true,
            defaultValue: '#dc2626',
            renderer: ColorPickerPreferenceItem,
          }),
        },
      },
      geologicTimePeriod: {
        title: '_GeologicTimePeriod',
        items: {
          treeAccentColor: defineItem({
            title: preferencesText('treeAccentColor'),
            requiresReload: false,
            visible: true,
            defaultValue: '#f79245',
            renderer: ColorPickerPreferenceItem,
          }),
          synonymColor: defineItem({
            title: preferencesText('synonymColor'),
            requiresReload: false,
            visible: true,
            defaultValue: '#dc2626',
            renderer: ColorPickerPreferenceItem,
          }),
        },
      },
      lithoStrat: {
        title: '_LithoStrat',
        items: {
          treeAccentColor: defineItem({
            title: preferencesText('treeAccentColor'),
            requiresReload: false,
            visible: true,
            defaultValue: '#f79245',
            renderer: ColorPickerPreferenceItem,
          }),
          synonymColor: defineItem({
            title: preferencesText('synonymColor'),
            requiresReload: false,
            visible: true,
            defaultValue: '#dc2626',
            renderer: ColorPickerPreferenceItem,
          }),
        },
      },
    },
  },
  queryBuilder: {
    title: queryText('queryBuilder'),
    subCategories: {
      general: {
        title: preferencesText('general'),
        items: {
          noRestrictionsMode: defineItem<boolean>({
            title: preferencesText('noRestrictionsMode'),
            description: preferencesText('noRestrictionsModeQueryDescription'),
            requiresReload: false,
            visible: 'adminsOnly',
            defaultValue: false,
            type: 'java.lang.Boolean',
          }),
          showNoReadTables: defineItem<boolean>({
            title: preferencesText('showNoReadTables'),
            requiresReload: false,
            visible: true,
            defaultValue: false,
            type: 'java.lang.Boolean',
          }),
        },
      },
      behavior: {
        title: preferencesText('behavior'),
        items: {
          stickyScrolling: defineItem<boolean>({
            title: preferencesText('stickyScrolling'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
        },
      },
      appearance: {
        title: preferencesText('appearance'),
        items: {
          condensedQueryResult: defineItem<boolean>({
            title: preferencesText('condensedQueryResult'),
            requiresReload: false,
            visible: true,
            defaultValue: false,
            type: 'java.lang.Boolean',
          }),
        },
      },
    },
  },
  reports: {
    title: commonText('reports'),
    subCategories: {
      behavior: {
        title: preferencesText('behavior'),
        items: {
          clearQueryFilters: defineItem<boolean>({
            title: preferencesText('clearQueryFilters'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
        },
      },
    },
  },
  workBench: {
    title: commonText('workBench'),
    subCategories: {
      editor: {
        title: preferencesText('spreadsheet'),
        items: {
          minSpareRows: defineItem<number>({
            title: preferencesText('minSpareRows'),
            requiresReload: false,
            visible: true,
            defaultValue: 1,
            type: 'java.lang.Integer',
            parser: {
              min: 0,
              max: 100,
            },
          }),
          autoWrapCol: defineItem<boolean>({
            title: preferencesText('autoWrapCols'),
            requiresReload: false,
            visible: true,
            defaultValue: false,
            type: 'java.lang.Boolean',
          }),
          autoWrapRow: defineItem<boolean>({
            title: preferencesText('autoWrapRows'),
            requiresReload: false,
            visible: true,
            defaultValue: false,
            type: 'java.lang.Boolean',
          }),
          tabMoveDirection: defineItem<'col' | 'row'>({
            title: preferencesText('tabMoveDirection'),
            description: preferencesText('tabMoveDirectionDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: 'col',
            values: [
              {
                value: 'col',
                title: preferencesText('column'),
              },
              {
                value: 'row',
                title: preferencesText('row'),
              },
            ],
          }),
          enterMoveDirection: defineItem<'col' | 'row'>({
            title: preferencesText('enterMoveDirection'),
            description: preferencesText('enterMoveDirectionDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: 'row',
            values: [
              {
                value: 'col',
                title: preferencesText('column'),
              },
              {
                value: 'row',
                title: preferencesText('row'),
              },
            ],
          }),
          enterBeginsEditing: defineItem<boolean>({
            title: preferencesText('enterBeginsEditing'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          filterPickLists: defineItem<
            'case-sensitive' | 'case-insensitive' | 'none'
          >({
            title: preferencesText('filterPickLists'),
            requiresReload: false,
            visible: true,
            defaultValue: 'none',
            values: [
              {
                value: 'none',
                title: commonText('no'),
              },
              {
                value: 'case-sensitive',
                title: preferencesText('caseSensitive'),
              },
              {
                value: 'case-insensitive',
                title: preferencesText('caseInsensitive'),
              },
            ],
          }),
        },
      },
      wbPlanView: {
        title: wbText('dataMapper'),
        items: {
          showNewDataSetWarning: defineItem<boolean>({
            title: preferencesText('showNewDataSetWarning'),
            description: preferencesText('showNewDataSetWarningDescription'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          noRestrictionsMode: defineItem<boolean>({
            title: preferencesText('noRestrictionsMode'),
            description: preferencesText('noRestrictionsModeWbDescription'),
            requiresReload: false,
            visible: 'adminsOnly',
            defaultValue: false,
            type: 'java.lang.Boolean',
          }),
          showNoAccessTables: defineItem<boolean>({
            title: preferencesText('showNoAccessTables'),
            requiresReload: false,
            visible: true,
            defaultValue: false,
            type: 'java.lang.Boolean',
          }),
        },
      },
    },
  },
  leaflet: {
    title: commonText('geoMap'),
    subCategories: {
      behavior: {
        title: preferencesText('behavior'),
        items: {
          doubleClickZoom: defineItem<boolean>({
            title: preferencesText('doubleClickZoom'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          closePopupOnClick: defineItem<boolean>({
            title: preferencesText('closePopupOnClick'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          animateTransitions: defineItem<boolean>({
            title: preferencesText('animateTransitions'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          panInertia: defineItem<boolean>({
            title: preferencesText('panInertia'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          mouseDrags: defineItem<boolean>({
            title: preferencesText('mouseDrags'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
          scrollWheelZoom: defineItem<boolean>({
            title: preferencesText('scrollWheelZoom'),
            requiresReload: false,
            visible: true,
            defaultValue: true,
            type: 'java.lang.Boolean',
          }),
        },
      },
    },
  },
  welcomePage: {
    title: preferencesText('welcomePage'),
    subCategories: {
      general: {
        title: preferencesText('general'),
        items: {
          mode: defineItem<WelcomePageMode>({
            title: preferencesText('content'),
            description: (
              <Link.NewTab href="https://github.com/specify/specify7/wiki/Customizing-the-splash-screen">
                {commonText('documentation')}
              </Link.NewTab>
            ),
            requiresReload: false,
            visible: true,
            defaultValue: 'default',
            renderer: WelcomePageModePreferenceItem,
          }),
          source: defineItem<string>({
            title: '',
            requiresReload: false,
            visible: false,
            defaultValue: defaultWelcomePageImage,
            type: 'text',
          }),
        },
      },
    },
  },
} as const;

// Use tree table labels as titles for the tree editor sections
import('../schema')
  .then(async ({ fetchContext, schema }) =>
    fetchContext.then(() => {
      const trees = preferenceDefinitions.treeEditor.subCategories;
      // @ts-expect-error Assigning to read-only
      trees.geography.title = schema.models.Geography.label;
      // @ts-expect-error Assigning to read-only
      trees.taxon.title = schema.models.Taxon.label;
      // @ts-expect-error Assigning to read-only
      trees.storage.title = schema.models.Storage.label;
      // @ts-expect-error Assigning to read-only
      trees.geologicTimePeriod.title = schema.models.GeologicTimePeriod.label;
      // @ts-expect-error Assigning to read-only
      trees.lithoStrat.title = schema.models.LithoStrat.label;
    })
  )
  .catch(crash);

export type Preferences = GenericPreferencesCategories &
  typeof preferenceDefinitions;

ensure<GenericPreferencesCategories>()(preferenceDefinitions);
