/*
 * WbPlanView logic for when the application is in the Mapping State
 * (when base table is selected and headers are loaded)
 *
 * @module
 */

import React from 'react';
import type { State } from 'typesafe-reducer';

import * as cache from '../cache';
import commonText from '../localization/common';
import wbText from '../localization/workbench';
import type { IR, RA } from '../types';
import type { ColumnOptions } from '../uploadplantomappingstree';
import { reducer } from '../wbplanviewmappingreducer';
import dataModelStorage from '../wbplanviewmodel';
import { findRequiredMissingFields } from '../wbplanviewmodelhelper';
import { getMappingLineData } from '../wbplanviewnavigator';
import {
  getAutoMapperSuggestions,
  getMappedFields,
  getMappingsTree,
  getMustMatchTables,
  goBack,
  mappingPathIsComplete,
} from '../wbplanviewutils';
import { useId } from './hooks';
import { LoadingScreen } from './modaldialog';
import type { Dataset } from './wbplanview';
import { handlePromiseReject } from './wbplanview';
import type { MappingPathProps } from './wbplanviewcomponents';
import { MappingLineComponent, ValidationButton } from './wbplanviewcomponents';
import { Layout } from './wbplanviewheader';
import {
  ChangeBaseTable,
  EmptyDataSetDialog,
  mappingOptionsMenu,
  MappingsControlPanel,
  MappingView,
  MustMatch,
  ReRunAutoMapper,
  ToggleMappingPath,
  ValidationResults,
} from './wbplanviewmappercomponents';

/*
 * Scope is used to differentiate between mapper definitions that should
 * be used by the autoMapper and suggestion boxes
 */
export type AutoMapperScope =
  // Used when selecting a base table
  | 'autoMapper'
  // Suggestion boxes - used when opening a picklist
  | 'suggestion';
export type MappingPath = RA<string>;
export type MappingPathWritable = string[];
export type FullMappingPath = Readonly<
  [...MappingPath, MappingType, string, ColumnOptions]
>;
/*
 * MappingType remains here from the time when we had `NewHeader` and
 *  `NewStaticHeader`. Also, it is not removed as it might be useful in the
 *  future if we would want to add new mapping types
 *
 */
export type MappingType = 'existingHeader';
export type RelationshipType =
  | 'one-to-one'
  | 'one-to-many'
  | 'many-to-one'
  | 'many-to-many';

export type SelectElementPosition = {
  readonly line: number;
  readonly index: number;
};

export type MappingLine = {
  readonly mappingType: MappingType;
  readonly headerName: string;
  readonly mappingPath: MappingPath;
  readonly columnOptions: ColumnOptions;
  readonly isFocused?: boolean;
};

export type AutoMapperSuggestion = MappingPathProps & {
  readonly mappingPath: MappingPath;
};

export type MappingState = State<
  'MappingState',
  {
    showMappingView: boolean;
    showHiddenFields: boolean;
    mappingView: MappingPath;
    mappingsAreValidated: boolean;
    lines: RA<MappingLine>;
    focusedLine: number;
    changesMade: boolean;
    mustMatchPreferences: IR<boolean>;
    autoMapperSuggestions?: RA<AutoMapperSuggestion>;
    openSelectElement?: SelectElementPosition;
    validationResults: RA<MappingPath>;
  }
>;

export const getDefaultMappingState = ({
  changesMade,
  lines,
  mustMatchPreferences,
}: {
  readonly changesMade: boolean;
  readonly lines: RA<MappingLine>;
  readonly mustMatchPreferences: IR<boolean>;
}): MappingState => ({
  type: 'MappingState',
  showHiddenFields: cache.get('wbPlanViewUi', 'showHiddenFields', {
    defaultValue: false,
  }),
  showMappingView: cache.get('wbPlanViewUi', 'showMappingView', {
    defaultValue: true,
  }),
  mappingView: ['0'],
  mappingsAreValidated: false,
  validationResults: [],
  lines,
  focusedLine: 0,
  changesMade,
  mustMatchPreferences,
});

export default function WbPlanViewMapper(props: {
  readonly readonly: boolean;
  readonly dataset: Dataset;
  readonly removeUnloadProtect: () => void;
  readonly setUnloadProtect: () => void;
  readonly baseTableName: string;
  readonly onChangeBaseTable: () => void;
  readonly onSave: (
    lines: RA<MappingLine>,
    mustMatchPreferences: IR<boolean>
  ) => Promise<void>;
  readonly onReRunAutoMapper: () => void;
  // Initial values for the state:
  readonly changesMade: boolean;
  readonly lines: RA<MappingLine>;
  readonly mustMatchPreferences: IR<boolean>;
}): JSX.Element {
  const [state, dispatch] = React.useReducer(
    reducer,
    {
      changesMade: props.changesMade,
      lines: props.lines,
      mustMatchPreferences: props.mustMatchPreferences,
    },
    getDefaultMappingState
  );

  // Set/unset unload protect
  React.useEffect(() => {
    if (state.changesMade) props.setUnloadProtect();
    else props.removeUnloadProtect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.changesMade]);

  const getMappedFieldsBind = getMappedFields.bind(undefined, state.lines);
  const listOfMappings = React.useRef<HTMLUListElement>(null);

  // Reposition suggestions box if it doesn't fit
  function repositionSuggestionBox(): void {
    if (
      typeof state.autoMapperSuggestions === 'undefined' ||
      state.autoMapperSuggestions.length === 0
    )
      return;

    if (listOfMappings.current === null) return;

    const autoMapperSuggestions = listOfMappings.current.getElementsByClassName(
      'custom-select-suggestion-list'
    )[0] as HTMLElement | undefined;

    if (!autoMapperSuggestions) return;

    const customSelectElement = autoMapperSuggestions.parentElement;

    if (!customSelectElement) return;

    const autoMapperSuggestionsHeight = autoMapperSuggestions.clientHeight;

    const listOfMappingsPosition = listOfMappings.current.offsetTop;
    const currentScrollTop = listOfMappings.current.scrollTop;
    const picklistPosition = customSelectElement.offsetTop;

    // Suggestions list fits on the screen. nothing to do
    if (
      picklistPosition - listOfMappingsPosition - autoMapperSuggestionsHeight >=
      0
    )
      return;

    if (!autoMapperSuggestions.classList.contains('controlled'))
      autoMapperSuggestions.classList.add('controlled');

    const suggestionsListPosition =
      picklistPosition - autoMapperSuggestionsHeight - currentScrollTop;

    const scrollPosition =
      picklistPosition - currentScrollTop - listOfMappingsPosition;

    // Hide suggestions box once its parent picklist becomes hidden
    autoMapperSuggestions.style.visibility =
      scrollPosition > 0 ? 'visible' : 'hidden';

    if (scrollPosition > 0)
      autoMapperSuggestions.style.top = `${suggestionsListPosition}px`;
  }

  React.useEffect(repositionSuggestionBox, [
    state.autoMapperSuggestions,
    listOfMappings,
  ]);

  React.useEffect(() => {
    window.addEventListener('resize', repositionSuggestionBox);
    return (): void =>
      window.removeEventListener('resize', repositionSuggestionBox);
  }, []);

  // Fetch automapper suggestions when opening a custom select element
  React.useEffect(() => {
    if (
      typeof state.openSelectElement === 'undefined' ||
      typeof state.lines[state.openSelectElement.line].mappingPath[
        state.openSelectElement.index
      ] === 'undefined'
    )
      return undefined;

    getAutoMapperSuggestions({
      lines: state.lines,
      line: state.openSelectElement.line,
      index: state.openSelectElement.index,
      baseTableName: props.baseTableName,
    })
      .then((autoMapperSuggestions) =>
        destructorCalled
          ? undefined
          : dispatch({
              type: 'AutoMapperSuggestionsLoadedAction',
              autoMapperSuggestions,
            })
      )
      .catch(console.error);

    let destructorCalled = false;
    return (): void => {
      destructorCalled = true;
    };
  }, [state.openSelectElement, props.baseTableName]);

  const id = useId('wbplanviewmapper');

  const validate = (): RA<MappingPath> =>
    findRequiredMissingFields(
      props.baseTableName,
      getMappingsTree(state.lines, true),
      state.mustMatchPreferences
    );

  function handleSave(ignoreValidation: boolean): void {
    const validationResults = ignoreValidation ? [] : validate();
    if (validationResults.length === 0) {
      setIsLoading(true);
      props
        .onSave(state.lines, state.mustMatchPreferences)
        .then(() => setIsLoading(false))
        .catch(handlePromiseReject);
    } else
      dispatch({
        type: 'ValidationAction',
        validationResults,
      });
  }

  const handleChange = (payload: {
    readonly line: 'mappingView' | number;
    readonly index: number;
    readonly close: boolean;
    readonly newValue: string;
    readonly isRelationship: boolean;
    readonly currentTableName: string;
    readonly newTableName: string;
  }): void =>
    dispatch({
      type: 'ChangeSelectElementValueAction',
      ...payload,
    });

  const handleClose = (): void =>
    dispatch({
      type: 'CloseSelectElementAction',
    });

  const [isLoading, setIsLoading] = React.useState(false);

  return isLoading ? (
    <LoadingScreen />
  ) : (
    <Layout
      readonly={props.readonly}
      title={
        <>
          <span title={wbText('dataSetName')}>{props.dataset.name}</span>
          <span title={wbText('baseTable')}>
            {` (${dataModelStorage.tables[props.baseTableName].label})`}
          </span>
        </>
      }
      buttonsLeft={
        props.readonly ? (
          <span
            className="v-center wbplanview-readonly-badge"
            title={wbText('dataSetUploadedDescription')}
          >
            {wbText('dataSetUploaded')}
          </span>
        ) : (
          <>
            <ChangeBaseTable onClick={props.onChangeBaseTable} />
            <button
              aria-haspopup="dialog"
              className="magic-button"
              type="button"
              onClick={(): void =>
                dispatch({
                  type: 'ResetMappingsAction',
                })
              }
            >
              {wbText('clearMappings')}
            </button>
            <ReRunAutoMapper
              showConfirmation={(): boolean =>
                state.lines.some(({ mappingPath }) =>
                  mappingPathIsComplete(mappingPath)
                )
              }
              onClick={props.onReRunAutoMapper}
            />
          </>
        )
      }
      buttonsRight={
        <>
          <ToggleMappingPath
            showMappingView={state.showMappingView}
            onClick={(): void =>
              dispatch({
                type: 'ToggleMappingViewAction',
                isVisible: !state.showMappingView,
              })
            }
          />
          <MustMatch
            readonly={props.readonly}
            getMustMatchPreferences={(): IR<boolean> =>
              getMustMatchTables({
                baseTableName: props.baseTableName,
                lines: state.lines,
                mustMatchPreferences: state.mustMatchPreferences,
              })
            }
            onChange={(mustMatchPreferences): void =>
              dispatch({
                type: 'MustMatchPrefChangeAction',
                mustMatchPreferences,
              })
            }
            onClose={(): void => {
              /*
               * Since setting table as must match causes all of it's fields to
               * be optional, we may have to rerun validation on
               * mustMatchPreferences changes
               */
              if (
                state.validationResults.length > 0 &&
                state.lines.some(({ mappingPath }) =>
                  mappingPathIsComplete(mappingPath)
                )
              )
                dispatch({
                  type: 'ValidationAction',
                  validationResults: validate(),
                });
            }}
          />
          {!props.readonly && (
            <ValidationButton
              canValidate={state.lines.some(({ mappingPath }) =>
                mappingPathIsComplete(mappingPath)
              )}
              isValidated={state.mappingsAreValidated}
              onClick={(): void =>
                dispatch({
                  type: 'ValidationAction',
                  validationResults: validate(),
                })
              }
            />
          )}
          <button
            type="button"
            aria-haspopup="dialog"
            className="magic-button"
            onClick={(): void => goBack(props.dataset.id)}
          >
            {props.readonly ? wbText('dataEditor') : commonText('cancel')}
          </button>
          {!props.readonly && (
            <button
              type="button"
              className="magic-button"
              disabled={!state.changesMade}
              onClick={(): void => handleSave(false)}
            >
              {commonText('save')}
            </button>
          )}
        </>
      }
      handleClick={handleClose}
    >
      {!props.readonly && state.validationResults.length > 0 && (
        <ValidationResults
          baseTableName={props.baseTableName}
          validationResults={state.validationResults}
          onSave={(): void => handleSave(true)}
          onDismissValidation={(): void =>
            dispatch({
              type: 'ValidationAction',
              validationResults: [],
            })
          }
          getMappedFields={getMappedFieldsBind}
          onValidationResultClick={(mappingPath: MappingPath): void =>
            dispatch({
              type: 'ValidationResultClickAction',
              mappingPath,
            })
          }
          mustMatchPreferences={state.mustMatchPreferences}
        />
      )}
      {state.showMappingView && (
        <MappingView
          baseTableName={props.baseTableName}
          focusedLineExists={state.lines.length > 0}
          mappingPath={state.mappingView}
          showHiddenFields={state.showHiddenFields}
          mapButtonIsEnabled={
            typeof state.focusedLine !== 'undefined' &&
            mappingPathIsComplete(state.mappingView)
          }
          readonly={props.readonly}
          mustMatchPreferences={state.mustMatchPreferences}
          handleMapButtonClick={
            props.readonly
              ? undefined
              : (): void => dispatch({ type: 'MappingViewMapAction' })
          }
          handleMappingViewChange={
            props.readonly
              ? undefined
              : (payload): void =>
                  handleChange({ line: 'mappingView', ...payload })
          }
          getMappedFields={getMappedFieldsBind}
        />
      )}

      <ul
        className="mapping-line-list"
        tabIndex={-1}
        ref={listOfMappings}
        onScroll={repositionSuggestionBox}
        aria-label={wbText('mappings')}
      >
        {state.lines.map(({ mappingPath, headerName, columnOptions }, line) => {
          const handleOpen = (index: number): void =>
            dispatch({
              type: 'OpenSelectElementAction',
              line,
              index,
            });

          const lineData = getMappingLineData({
            baseTableName: props.baseTableName,
            mappingPath,
            generateLastRelationshipData: true,
            iterate: true,
            customSelectType: 'CLOSED_LIST',
            handleChange: props.readonly
              ? undefined
              : (payload): void => handleChange({ line, ...payload }),
            handleOpen,
            handleClose,
            handleAutoMapperSuggestionSelection: props.readonly
              ? undefined
              : (suggestion: string): void =>
                  dispatch({
                    type: 'AutoMapperSuggestionSelectedAction',
                    suggestion,
                  }),
            getMappedFields: getMappedFieldsBind,
            openSelectElement:
              state.openSelectElement?.line === line
                ? state.openSelectElement
                : undefined,
            showHiddenFields: state.showHiddenFields,
            autoMapperSuggestions:
              (!props.readonly && state.autoMapperSuggestions) || [],
            mustMatchPreferences: state.mustMatchPreferences,
            columnOptions,
            mappingOptionsMenuGenerator: () =>
              mappingOptionsMenu({
                id: (suffix) => id(`column-options-${line}-${suffix}`),
                readonly: props.readonly,
                columnOptions,
                onChangeMatchBehaviour: (matchBehavior) =>
                  dispatch({
                    type: 'ChangeMatchBehaviorAction',
                    line,
                    matchBehavior,
                  }),
                onToggleAllowNulls: (allowNull) =>
                  dispatch({
                    type: 'ToggleAllowNullsAction',
                    line,
                    allowNull,
                  }),
                onChangeDefaultValue: (defaultValue) =>
                  dispatch({
                    type: 'ChangeDefaultValue',
                    line,
                    defaultValue,
                  }),
              }),
          });
          return (
            <MappingLineComponent
              key={line}
              headerName={headerName}
              readonly={props.readonly}
              isFocused={line === state.focusedLine}
              onFocus={(): void =>
                dispatch({
                  type: 'FocusLineAction',
                  line,
                })
              }
              onKeyDown={(key): void => {
                const openSelectElement =
                  state.openSelectElement?.line === line
                    ? state.openSelectElement.index
                    : undefined;

                if (typeof openSelectElement === 'number') {
                  if (key === 'ArrowLeft')
                    if (openSelectElement > 0)
                      handleOpen(openSelectElement - 1);
                    else
                      dispatch({
                        type: 'CloseSelectElementAction',
                      });
                  else if (key === 'ArrowRight')
                    if (openSelectElement + 1 < lineData.length)
                      handleOpen(openSelectElement + 1);
                    else
                      dispatch({
                        type: 'CloseSelectElementAction',
                      });

                  return;
                }

                if (key === 'ArrowLeft') handleOpen(lineData.length - 1);
                else if (key === 'ArrowRight' || key === 'Enter') handleOpen(0);
                else if (key === 'ArrowUp' && line > 0)
                  dispatch({
                    type: 'FocusLineAction',
                    line: line - 1,
                  });
                else if (key === 'ArrowDown' && line + 1 < state.lines.length)
                  dispatch({
                    type: 'FocusLineAction',
                    line: line + 1,
                  });
              }}
              onClearMapping={(): void =>
                dispatch({
                  type: 'ClearMappingLineAction',
                  line,
                })
              }
              lineData={lineData}
            />
          );
        })}
      </ul>

      <MappingsControlPanel
        showHiddenFields={state.showHiddenFields}
        onToggleHiddenFields={(): void =>
          dispatch({ type: 'ToggleHiddenFieldsAction' })
        }
        onAddNewHeader={
          props.readonly
            ? undefined
            : (newHeaderName): void => {
                dispatch({ type: 'AddNewHeaderAction', newHeaderName });
                // Scroll listOfMappings to the bottom
                if (listOfMappings.current)
                  listOfMappings.current.scrollTop =
                    listOfMappings.current.scrollHeight;
              }
        }
      />
      <EmptyDataSetDialog lineCount={state.lines.length} />
    </Layout>
  );
}
