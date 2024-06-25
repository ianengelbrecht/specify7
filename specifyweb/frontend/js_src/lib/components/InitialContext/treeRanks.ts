/**
 * Fetch tree definitions (and tree ranks) for all fields accessible in a
 * given discipline.
 */

import { f } from '../../utils/functools';
import type { RA } from '../../utils/types';
import { defined } from '../../utils/types';
import { caseInsensitiveHash, sortFunction } from '../../utils/utils';
import { fetchCollection, fetchRelated } from '../DataModel/collection';
import type {
  AnySchema,
  AnyTree,
  SerializedResource,
} from '../DataModel/helperTypes';
import type { SpecifyResource } from '../DataModel/legacyTypes';
import { fetchContext as fetchDomain, schema } from '../DataModel/schema';
import { getDomainResource } from '../DataModel/scoping';
import { genericTables } from '../DataModel/tables';
import type { Tables } from '../DataModel/types';

let treeDefinitions: {
  readonly [TREE_NAME in AnyTree['tableName']]: RA<{
    readonly definition: SpecifyResource<Tables[`${TREE_NAME}TreeDef`]>;
    readonly ranks: RA<SerializedResource<Tables[`${TREE_NAME}TreeDefItem`]>>;
  }>;
} = undefined!;

/*
 * FEATURE: allow reordering trees
 *    See https://github.com/specify/specify7/issues/2121#issuecomment-1432158152
 */
const commonTrees = ['Geography', 'Storage', 'Taxon'] as const;
const treesForPaleo = ['GeologicTimePeriod', 'LithoStrat'] as const;
export const allTrees = [...commonTrees, ...treesForPaleo] as const;
const paleoDiscs = new Set(['paleobotany', 'invertpaleo', 'vertpaleo']);
/*
 * Until discipline information is loaded, assume all trees are appropriate in
 * this discipline
 */
let disciplineTrees: RA<AnyTree['tableName']> = allTrees;
export const getDisciplineTrees = (): typeof disciplineTrees => disciplineTrees;

export const isTreeTable = (
  tableName: keyof Tables
): tableName is AnyTree['tableName'] => f.includes(allTrees, tableName);

export const isTreeResource = (
  resource: SpecifyResource<AnySchema>
): resource is SpecifyResource<AnyTree> =>
  f.includes(allTrees, resource.specifyTable.name);

export const treeRanksPromise = Promise.all([
  // Dynamic imports are used to prevent circular dependencies
  import('../Permissions/helpers'),
  import('../Permissions').then(async ({ fetchContext }) => fetchContext),
  import('../DataModel/tables').then(async ({ fetchContext }) => fetchContext),
  fetchDomain,
])
  .then(async ([{ hasTreeAccess, hasTablePermission }]) =>
    hasTablePermission('Discipline', 'read')
      ? getDomainResource('discipline')
          ?.fetch()
          .then((discipline) => {
            if (!f.has(paleoDiscs, discipline?.get('type')))
              disciplineTrees = commonTrees;
          })
          .then(async () =>
            Promise.all(
              disciplineTrees
                .filter((treeName) => hasTreeAccess(treeName, 'read'))
                .map(
                  async (treeName) =>
                    [
                      treeName,
                      await fetchCollection(`${treeName}TreeDef`, {
                        domainFilter: true,
                        limit: 0,
                      }).then(async ({ records }) =>
                        Promise.all(
                          records.map(async (definition) => ({
                            definition,
                            ranks: await fetchRelated(
                              definition,
                              'treeDefItems',
                              0
                            ).then(({ records }) =>
                              Array.from(records).sort(
                                sortFunction(({ rankId }) => rankId)
                              )
                            ),
                          }))
                        )
                      ),
                    ] as const
                )
            )
          )
      : []
  )
  .then((results) => {
    // @ts-expect-error
    treeDefinitions = Object.fromEntries(results.filter(Boolean));
    return treeDefinitions;
  });

function getTreeScope(
  treeName: AnyTree['tableName']
): keyof typeof schema['domainLevelIds'] | undefined {
  const treeRelationships = new Set(
    genericTables[`${treeName}TreeDef`].relationships.map(({ relatedTable }) =>
      relatedTable.name.toLowerCase()
    )
  );
  return Object.keys(schema.domainLevelIds).find((domainTable) =>
    treeRelationships.has(domainTable)
  );
}

export function getTreeDefinitionItems<TREE_NAME extends AnyTree['tableName']>(
  tableName: TREE_NAME,
  includeRoot: boolean
): typeof treeDefinitions[TREE_NAME]['ranks'] | undefined {
  const definition = caseInsensitiveHash(treeDefinitions, tableName);
  return definition?.ranks.slice(includeRoot ? 0 : 1);
}

export const strictGetTreeDefinitionItems = <
  TREE_NAME extends AnyTree['tableName']
>(
  tableName: TREE_NAME,
  includeRoot: boolean
): typeof treeDefinitions[TREE_NAME]['ranks'] =>
  defined(
    getTreeDefinitionItems(tableName, includeRoot),
    `Unable to get tree ranks for a ${tableName} table`
  );

export const exportsForTests = {
  getTreeScope,
};
