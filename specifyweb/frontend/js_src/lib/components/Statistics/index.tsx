import React from 'react';
import type { State } from 'typesafe-reducer';

import { useErrorContext } from '../../hooks/useErrorContext';
import { commonText } from '../../localization/common';
import { statsText } from '../../localization/stats';
import { cleanMaybeFulfilled } from '../../utils/ajax/throttledPromise';
import { f } from '../../utils/functools';
import type { RA } from '../../utils/types';
import { getUniqueName } from '../../utils/uniquifyName';
import { removeItem, removeKey, replaceItem } from '../../utils/utils';
import { H2, H3, Ul } from '../Atoms';
import { Button } from '../Atoms/Button';
import { className } from '../Atoms/className';
import { Form } from '../Atoms/Form';
import { Submit } from '../Atoms/Submit';
import { softFail } from '../Errors/Crash';
import { useMenuItem } from '../Header/useMenuItem';
import { userInformation } from '../InitialContext/userInformation';
import { DateElement } from '../Molecules/DateElement';
import { downloadFile } from '../Molecules/FilePicker';
import { hasPermission } from '../Permissions/helpers';
import { collectionPreferences } from '../Preferences/collectionPreferences';
import { userPreferences } from '../Preferences/userPreferences';
import { useQueries } from '../Toolbar/Query';
import { defaultLayoutTest } from './__tests__/layout.tests';
import { AddStatDialog } from './AddStatDialog';
import { StatsAsideButton } from './Buttons';
import { Categories } from './Categories';
import {
  getDynamicCategoriesToFetch,
  getOffsetOne,
  statsToTsv,
  useBackendApi,
  useDefaultDynamicCategorySetter,
  useDefaultStatsToAdd,
  useDynamicCategorySetter,
} from './hooks';
import { StatsPageEditing } from './StatsPageEditing';
import { defaultLayoutGenerated, dynamicStatsSpec } from './StatsSpec';
import type { CustomStat, DefaultStat, StatLayout } from './types';

export function StatsPage(): JSX.Element | null {
  useMenuItem('statistics');
  const [collectionLayout, setCollectionLayout] = collectionPreferences.use(
    'statistics',
    'appearance',
    'layout'
  );

  const [personalLayout, setPersonalLayout] = userPreferences.use(
    'statistics',
    'appearance',
    'layout'
  );

  const [defaultLayout, setDefaultLayout] = React.useState<
    RA<StatLayout> | undefined
  >(undefined);
  const layout = {
    [statsText.shared()]: collectionLayout,
    [statsText.private()]: personalLayout,
  };

  const [state, setState] = React.useState<
    | State<
        'AddingState',
        {
          readonly pageIndex: number;
          readonly categoryIndex: number;
        }
      >
    | State<
        'DeletingCategoryState',
        { readonly categoryContainsCustom: boolean }
      >
    | State<
        'PageRenameState',
        {
          readonly pageIndex: number | undefined;
          readonly isShared: boolean;
        }
      >
    | State<'DefaultState'>
    | State<'EditingState'>
  >({ type: 'DefaultState' });

  const isAddingItem = state.type === 'AddingState';
  const isEditing =
    state.type === 'EditingState' ||
    isAddingItem ||
    state.type === 'PageRenameState';

  const hasEditPermission = hasPermission(
    '/preferences/statistics',
    'edit_protected'
  );

  const canEditIndex = (isCollection: boolean): boolean =>
    isCollection ? hasEditPermission : true;

  const [activePage, setActivePage] = React.useState<{
    readonly isShared: boolean;
    readonly pageIndex: number;
  }>({
    isShared: true,
    pageIndex: 0,
  });

  const errorContextState = React.useMemo(
    () => ({
      shared: collectionLayout,
      personal: personalLayout,
      default: defaultLayout,
      onShared: activePage.isShared,
      pageIndex: activePage.pageIndex,
      state,
    }),
    [
      collectionLayout,
      personalLayout,
      defaultLayout,
      activePage.isShared,
      activePage.pageIndex,
      state,
    ]
  );

  useErrorContext('statistics', errorContextState);

  const getSourceLayoutSetter = (isShared: boolean) =>
    isShared ? setCollectionLayout : setPersonalLayout;

  const setCurrentLayout = getSourceLayoutSetter(activePage.isShared);

  const getSourceLayout = (isShared: boolean) =>
    isShared ? collectionLayout : personalLayout;

  const sourceLayout = getSourceLayout(activePage.isShared);

  const allCategories = React.useMemo(
    () => dynamicStatsSpec.map(({ responseKey }) => responseKey),
    []
  );
  const [categoriesToFetch, setCategoriesToFetch] = React.useState<RA<string>>(
    []
  );

  const [defaultCategoriesToFetch, setDefaultCategoriesToFetch] =
    React.useState<RA<string>>([]);

  React.useEffect(() => {
    const absentDynamicCategories =
      sourceLayout === undefined
        ? []
        : getDynamicCategoriesToFetch(sourceLayout);
    const notCurrentlyFetching = absentDynamicCategories.filter(
      (category) => !categoriesToFetch.includes(category)
    );
    if (notCurrentlyFetching.length > 0) {
      setCategoriesToFetch([...categoriesToFetch, ...notCurrentlyFetching]);
    }
  }, [sourceLayout, categoriesToFetch, setCategoriesToFetch]);

  const backEndResponse = useBackendApi(categoriesToFetch);
  const defaultBackEndResponse = useBackendApi(defaultCategoriesToFetch);

  /*
   * Initial Load For Collection and Personal Pages
   * If collection and personal layout are undefined initially, then we need to
   * fetch all unknown categories.
   * It is simpler to make the promise twice since throttledPromise returns the
   * previous promise if the spec is same
   */
  React.useEffect(() => {
    if (collectionLayout === undefined) {
      setCollectionLayout([defaultLayoutGenerated[0]]);
    }
  }, [collectionLayout, setCollectionLayout]);

  React.useEffect(() => {
    if (personalLayout === undefined) {
      setPersonalLayout([defaultLayoutGenerated[1]]);
    }
  }, [setPersonalLayout, personalLayout]);

  /* Set Default Layout every time page is started from scratch*/
  React.useEffect(() => {
    setDefaultLayout(defaultLayoutGenerated);
  }, [setDefaultLayout]);

  const pageLastUpdated = activePage.isShared
    ? collectionLayout?.[activePage.pageIndex].lastUpdated
    : personalLayout?.[activePage.pageIndex].lastUpdated;

  const canEdit = !activePage.isShared || hasEditPermission;

  const pageLayout = activePage.isShared
    ? collectionLayout?.[activePage.pageIndex].categories === undefined
      ? undefined
      : collectionLayout[activePage.pageIndex]
    : personalLayout?.[activePage.pageIndex].categories === undefined
    ? undefined
    : personalLayout[activePage.pageIndex];

  const handleChange = React.useCallback(
    (
      newCategories: (
        oldCategory: StatLayout['categories']
      ) => StatLayout['categories']
    ): void =>
      setCurrentLayout((oldLayout: RA<StatLayout> | undefined) =>
        oldLayout === undefined
          ? undefined
          : replaceItem(oldLayout, activePage.pageIndex, {
              ...oldLayout[activePage.pageIndex],
              categories: newCategories(
                oldLayout[activePage.pageIndex].categories
              ),
            })
      ),
    [activePage.pageIndex, activePage.isShared]
  );

  if (process.env.NODE_ENV === 'development') {
    console.log('Layout Updates');
    console.log(defaultLayoutTest);
  }
  // Used to set unknown categories once for layout initially, and every time for default layout
  useDynamicCategorySetter(backEndResponse, handleChange, categoriesToFetch);
  useDefaultDynamicCategorySetter(defaultBackEndResponse, setDefaultLayout);

  const filters = React.useMemo(
    () => ({
      specifyUser: userInformation.id,
    }),
    []
  );
  const queries = useQueries(filters, false);
  const previousCollectionLayout = React.useRef(
    collectionLayout as unknown as RA<StatLayout>
  );
  const previousLayout = React.useRef(
    personalLayout as unknown as RA<StatLayout>
  );

  const defaultStatsAddLeft = useDefaultStatsToAdd(
    layout[activePage.isShared ? statsText.shared() : statsText.private()]?.[
      activePage.pageIndex
    ],
    defaultLayout
  );

  const getValueUndefined = (layout: StatLayout): StatLayout => ({
    label: layout.label,
    categories: layout.categories.map((category) => ({
      label: category.label,
      items: category.items?.map((item) => ({
        ...item,
        itemValue: undefined,
      })),
    })),
    lastUpdated: undefined,
  });

  const [refreshLayout, setRefreshLayout] = React.useState(true);
  React.useLayoutEffect(() => {
    if (refreshLayout) {
      setCollectionLayout((layout) =>
        layout === undefined
          ? undefined
          : layout.map((pageLayout) => getValueUndefined(pageLayout))
      );
      setPersonalLayout((layout) =>
        layout === undefined
          ? undefined
          : layout.map((pageLayout) => getValueUndefined(pageLayout))
      );
    }
    setRefreshLayout(false);
    return () => {
      cleanMaybeFulfilled();
    };
  }, [refreshLayout, setRefreshLayout]);
  React.useLayoutEffect(() => {
    setCurrentLayout((layout) =>
      layout === undefined
        ? undefined
        : layout.map((pageLayout, pageIndex) => {
            const date = new Date();
            return {
              ...pageLayout,
              lastUpdated:
                pageLayout.lastUpdated === undefined &&
                pageIndex === activePage.pageIndex
                  ? date.toJSON()
                  : pageLayout.lastUpdated,
            };
          })
    );
  }, [
    activePage.pageIndex,
    activePage.isShared,
    pageLastUpdated,
    setCurrentLayout,
    refreshLayout,
  ]);
  const handleAdd = (
    item: CustomStat | DefaultStat,
    categoryIndex?: number,
    itemIndex?: number
  ): void =>
    handleChange((oldCategory) =>
      replaceItem(oldCategory, categoryIndex ?? -1, {
        ...oldCategory[categoryIndex ?? -1],
        items:
          itemIndex === undefined || itemIndex === -1
            ? [...oldCategory[categoryIndex ?? -1].items, modifyName(item)]
            : replaceItem(
                oldCategory[categoryIndex ?? -1].items,
                itemIndex,
                item
              ),
      })
    );

  const modifyName = (
    item: CustomStat | DefaultStat
  ): CustomStat | DefaultStat => {
    if (pageLayout === undefined) {
      return item;
    }
    const itemsLabelMatched = pageLayout.categories
      .flatMap(({ items }) => items)
      .map((anyItem) => anyItem.label)
      .filter(Boolean);
    return {
      ...item,
      label: getUniqueName(item.label, itemsLabelMatched),
    };
  };

  const handleDefaultLoad = React.useCallback(
    (
      pageIndex: number,
      categoryIndex: number,
      itemIndex: number,
      value: number | string
    ) =>
      setDefaultLayout((oldValue) =>
        f.maybe(oldValue, (oldValue) =>
          replaceItem(oldValue, pageIndex, {
            ...oldValue[pageIndex],
            categories: replaceItem(
              oldValue[pageIndex].categories,
              categoryIndex,
              {
                ...oldValue[pageIndex].categories[categoryIndex],
                items: replaceItem(
                  oldValue[pageIndex].categories[categoryIndex].items,
                  itemIndex,
                  {
                    ...oldValue[pageIndex].categories[categoryIndex].items[
                      itemIndex
                    ],
                    itemValue: value,
                  }
                ),
              }
            ),
          })
        )
      ),
    [setDefaultLayout]
  );
  const handleLoad = React.useCallback(
    (categoryIndex: number, itemIndex: number, value: number | string) =>
      handleChange((oldCategory) =>
        replaceItem(oldCategory, categoryIndex, {
          ...oldCategory[categoryIndex],
          items: replaceItem(oldCategory[categoryIndex].items, itemIndex, {
            ...oldCategory[categoryIndex].items[itemIndex],
            itemValue: value,
          }),
        })
      ),
    [handleChange]
  );

  const refreshPage = () => {
    cleanMaybeFulfilled();
    setCurrentLayout((layout) =>
      layout === undefined
        ? undefined
        : replaceItem(
            layout,
            activePage.pageIndex,
            getValueUndefined(layout[activePage.pageIndex])
          )
    );
    setCategoriesToFetch([]);
  };

  return collectionLayout === undefined ? null : (
    <Form
      className={`${className.containerFullGray} md:overflow-y-none overflow-y-auto`}
      onSubmit={(): void => {
        setState({ type: 'DefaultState' });
        Promise.all([
          userPreferences.awaitSynced(),
          collectionPreferences.awaitSynced(),
        ]).catch(softFail);
      }}
    >
      <div className="flex flex-wrap items-center gap-2">
        <H2 className="text-2xl">{statsText.statistics()}</H2>
        <span className="-ml-2 flex-1" />
        {pageLastUpdated !== undefined && (
          <span>
            {`${statsText.lastRefreshed()} `}
            <DateElement date={pageLastUpdated} />
          </span>
        )}
        <Button.Gray onClick={(): void => refreshPage()}>
          {statsText.refresh()}
        </Button.Gray>
        {Object.values(layout).every((layouts) => layouts !== undefined) && (
          <Button.Gray
            onClick={(): void => {
              const date = new Date();
              const sourceIndex = activePage.isShared ? 0 : 1;
              const pageIndex = activePage.pageIndex;
              const statsTsv = statsToTsv(
                layout,
                activePage.isShared ? 0 : 1,
                activePage.pageIndex
              );
              const sourceName = Object.keys(layout)[sourceIndex];
              const pageName =
                Object.values(layout)[sourceIndex]?.[pageIndex].label;
              const fileName = `Specify 7 Statistics ${sourceName} ${
                pageName ?? ''
              } ${date.toDateString()} ${
                date.toTimeString().split(' ')[0]
              }.tsv`;
              downloadFile(fileName, statsTsv).catch(softFail);
            }}
          >
            {statsText.downloadAsTSV()}
          </Button.Gray>
        )}
        {isEditing ? (
          <>
            {process.env.NODE_ENV === 'development' && (
              <Button.Gray
                onClick={(): void => {
                  cleanMaybeFulfilled();
                  setCollectionLayout(undefined);
                  setPersonalLayout(undefined);
                  setCategoriesToFetch([]);
                  setActivePage({ isShared: true, pageIndex: 0 });
                  setRefreshLayout(true);
                }}
              >
                {`${commonText.reset()} [DEV]`}
              </Button.Gray>
            )}

            <Button.Gray
              onClick={(): void => {
                setCollectionLayout(previousCollectionLayout.current);
                setPersonalLayout(previousLayout.current);
                setState({ type: 'DefaultState' });
                setActivePage(({ isShared, pageIndex }) => {
                  /*
                   * Also handles cases where a new page is added and user clicks on cancel.
                   * Shifts to the last page in the current group
                   */
                  const previousLayoutRef = isShared
                    ? previousCollectionLayout
                    : previousLayout;
                  const newIndex = Math.min(
                    pageIndex,
                    previousLayoutRef.current.length - 1
                  );
                  return {
                    isShared,
                    pageIndex: newIndex,
                  };
                });
              }}
            >
              {commonText.cancel()}
            </Button.Gray>
            <Submit.Gray>{commonText.save()}</Submit.Gray>
          </>
        ) : (
          canEdit && (
            <Button.Gray
              onClick={(): void => {
                setState({
                  type: 'EditingState',
                });
                if (collectionLayout !== undefined)
                  previousCollectionLayout.current = collectionLayout;
                if (personalLayout !== undefined)
                  previousLayout.current = personalLayout;
              }}
            >
              {commonText.edit()}
            </Button.Gray>
          )
        )}
      </div>
      <div className="flex flex-col md:overflow-hidden">
        <div className="flex flex-col gap-2 overflow-y-hidden md:flex-row">
          <aside
            className={`
                 top-0 flex min-w-fit flex-1 flex-col divide-y-4 !divide-[color:var(--form-background)]
                  md:sticky
              `}
          >
            <Ul className="flex flex-col gap-2">
              {Object.entries(layout).map(
                ([parentLayoutName, parentLayout], index) =>
                  parentLayout === undefined ? undefined : (
                    <li className="flex flex-col gap-2" key={index}>
                      <H3 className="text-xl font-bold">{parentLayoutName}</H3>
                      <Ul className="flex flex-col gap-2">
                        {parentLayout.map(({ label }, pageIndex) => (
                          <li key={pageIndex}>
                            <StatsAsideButton
                              isCurrent={
                                activePage.pageIndex === pageIndex &&
                                activePage.isShared === (index === 0)
                              }
                              label={label}
                              onClick={(): void =>
                                setActivePage({
                                  isShared: index === 0,
                                  pageIndex,
                                })
                              }
                              onRename={
                                isEditing && canEditIndex(index === 0)
                                  ? (): void =>
                                      setState({
                                        type: 'PageRenameState',
                                        isShared: index === 0,
                                        pageIndex,
                                      })
                                  : undefined
                              }
                            />
                          </li>
                        ))}

                        {isEditing && canEditIndex(index === 0) && (
                          <Button.Small
                            className="max-w-fit"
                            name={commonText.add()}
                            variant={className.blueButton}
                            onClick={(): void =>
                              setState({
                                type: 'PageRenameState',
                                pageIndex: undefined,
                                isShared: index === 0,
                              })
                            }
                          >
                            {commonText.add()}
                          </Button.Small>
                        )}
                      </Ul>
                    </li>
                  )
              )}
            </Ul>
          </aside>
          {state.type === 'PageRenameState' && (
            <StatsPageEditing
              label={
                typeof state.pageIndex === 'number'
                  ? state.isShared
                    ? collectionLayout[state.pageIndex].label
                    : personalLayout?.[state.pageIndex].label
                  : undefined
              }
              onAdd={
                typeof state.pageIndex === 'number'
                  ? undefined
                  : (label): void => {
                      const targetSourceLayout = getSourceLayout(
                        state.isShared
                      );
                      getSourceLayoutSetter(state.isShared)((layout) =>
                        layout === undefined
                          ? undefined
                          : [
                              ...layout,
                              {
                                label,
                                categories: [],
                                lastUpdated: undefined,
                              },
                            ]
                      );
                      setState({
                        type: 'EditingState',
                      });
                      if (targetSourceLayout !== undefined) {
                        setActivePage({
                          pageIndex: targetSourceLayout.length,
                          isShared: state.isShared,
                        });
                      }
                    }
              }
              onClose={(): void => setState({ type: 'EditingState' })}
              onRemove={
                state.pageIndex === undefined ||
                (getSourceLayout(state.isShared) ?? []).length <= 1
                  ? undefined
                  : () => {
                      const targetSourceLayout = getSourceLayout(
                        state.isShared
                      );
                      if (
                        targetSourceLayout !== undefined &&
                        state.pageIndex !== undefined
                      ) {
                        getSourceLayoutSetter(state.isShared)((oldLayout) =>
                          oldLayout === undefined
                            ? undefined
                            : removeItem(oldLayout, state.pageIndex!)
                        );
                        setState({
                          type: 'EditingState',
                        });
                        setActivePage({
                          pageIndex:
                            activePage.isShared === state.isShared
                              ? getOffsetOne(
                                  activePage.pageIndex,
                                  state.pageIndex
                                )
                              : activePage.pageIndex,
                          isShared: activePage.isShared,
                        });
                      }
                    }
              }
              onRename={
                state.pageIndex === undefined
                  ? undefined
                  : (value) => {
                      const targetSourceLayout = getSourceLayout(
                        state.isShared
                      );
                      if (targetSourceLayout !== undefined) {
                        getSourceLayoutSetter(state.isShared)((layout) =>
                          layout === undefined || state.pageIndex === undefined
                            ? undefined
                            : replaceItem(layout, state.pageIndex, {
                                ...layout[state.pageIndex],
                                label: value,
                              })
                        );
                      }
                      setState({
                        type: 'EditingState',
                      });
                    }
              }
            />
          )}
          <div className="grid w-full grid-cols-[repeat(auto-fill,minmax(20rem,1fr))] gap-4 overflow-y-auto px-4 pb-6">
            <Categories
              pageLayout={pageLayout}
              onAdd={
                isEditing && canEditIndex(activePage.isShared)
                  ? (categoryindex): void =>
                      typeof categoryindex === 'number'
                        ? setState({
                            type: 'AddingState',
                            pageIndex: activePage.pageIndex,
                            categoryIndex: categoryindex,
                          })
                        : handleChange((oldCategory) => [
                            ...oldCategory,
                            {
                              label: '',
                              items: [],
                            },
                          ])
                  : undefined
              }
              onCategoryRename={
                isEditing && canEditIndex(activePage.isShared)
                  ? (newName, categoryIndex): void =>
                      handleChange((oldCategory) =>
                        replaceItem(oldCategory, categoryIndex, {
                          ...oldCategory[categoryIndex],
                          label: newName,
                        })
                      )
                  : undefined
              }
              onClick={handleAdd}
              onEdit={
                isEditing
                  ? undefined
                  : (categoryIndex, itemIndex, querySpec): void =>
                      handleChange((oldCategory) =>
                        replaceItem(oldCategory, categoryIndex, {
                          ...oldCategory[categoryIndex],
                          items: replaceItem(
                            oldCategory[categoryIndex].items,
                            itemIndex,
                            {
                              ...oldCategory[categoryIndex].items[itemIndex],
                              ...(oldCategory[categoryIndex].items[itemIndex]
                                .type === 'DefaultStat'
                                ? {}
                                : {
                                    querySpec,
                                    itemValue: undefined,
                                  }),
                            }
                          ),
                        })
                      )
              }
              onLoad={handleLoad}
              onRemove={(categoryIndex, itemIndex): void =>
                handleChange((oldCategory) =>
                  typeof itemIndex === 'number'
                    ? replaceItem(oldCategory, categoryIndex, {
                        ...oldCategory[categoryIndex],
                        items: removeItem(
                          oldCategory[categoryIndex].items,
                          itemIndex
                        ),
                      })
                    : removeItem(oldCategory, categoryIndex)
                )
              }
              onRename={
                isEditing && canEditIndex(activePage.isShared)
                  ? (categoryIndex, itemIndex, newLabel): void =>
                      handleChange((oldCategory) =>
                        replaceItem(oldCategory, categoryIndex, {
                          ...oldCategory[categoryIndex],
                          items: replaceItem(
                            oldCategory[categoryIndex].items,
                            itemIndex,
                            {
                              ...oldCategory[categoryIndex].items[itemIndex],
                              label: newLabel,
                            }
                          ),
                        })
                      )
                  : undefined
              }
            />
          </div>
        </div>
      </div>

      {state.type === 'AddingState' && (
        <AddStatDialog
          defaultStatsAddLeft={defaultStatsAddLeft}
          queries={queries}
          onInitialLoad={() => setDefaultCategoriesToFetch(allCategories)}
          onAdd={(item, itemIndex): void => {
            handleAdd(item, state.categoryIndex, itemIndex);
          }}
          onClose={(): void => {
            setState({
              type: 'EditingState',
            });
            setDefaultLayout((layout) =>
              layout === undefined
                ? undefined
                : layout.map(({ label, categories, lastUpdated }) => ({
                    label,
                    categories: categories.map(({ label, items }) => ({
                      label,
                      items: items?.map((item) =>
                        item.type === 'DefaultStat'
                          ? (removeKey(item, 'isVisible') as DefaultStat)
                          : item
                      ),
                    })),
                    lastUpdated,
                  }))
            );
          }}
          onLoad={handleDefaultLoad}
        />
      )}
    </Form>
  );
}
