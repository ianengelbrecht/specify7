import { formsText } from '../../localization/forms';
import { resourcesText } from '../../localization/resources';
import { f } from '../../utils/functools';
import { relationshipIsToMany } from '../WbPlanView/mappingHelpers';
import type { BusinessRuleResult } from './businessRules';
import type { AnySchema, TableFields } from './helperTypes';
import {
  checkPrepAvailability,
  getTotalLoaned,
  getTotalResolved,
  getTotalReturned,
  previousLoanPreparations,
  updateLoanPrep,
} from './interactionBusinessRules';
import type { SpecifyResource } from './legacyTypes';
import { setSaveBlockers } from './saveBlockers';
import type { Collection } from './specifyTable';
import { tables } from './tables';
import type {
  Address,
  BorrowMaterial,
  CollectionObject,
  CollectionObjectType,
  Determination,
  DNASequence,
  LoanPreparation,
  LoanReturnPreparation,
  Tables,
  Taxon,
} from './types';

export type BusinessRuleDefs<SCHEMA extends AnySchema> = {
  readonly onAdded?: (
    resource: SpecifyResource<SCHEMA>,
    collection: Collection<SCHEMA>
  ) => void;
  readonly onRemoved?: (
    resource: SpecifyResource<SCHEMA>,
    collection: Collection<SCHEMA>
  ) => void;
  readonly customInit?: (resource: SpecifyResource<SCHEMA>) => void;
  readonly fieldChecks?: {
    readonly [FIELD_NAME in TableFields<SCHEMA>]?: (
      resource: SpecifyResource<SCHEMA>
    ) => Promise<BusinessRuleResult | undefined> | void;
  };
};

type MappedBusinessRuleDefs = {
  readonly [TABLE in keyof Tables]?: BusinessRuleDefs<Tables[TABLE]>;
};

const CURRENT_DETERMINATION_KEY = 'determination-isCurrent';
const DETERMINATION_TAXON_KEY = 'determination-taxon';

const hasNoCurrentDetermination = (collection: Collection<Determination>) =>
  collection.models.length > 0 &&
  !collection.models.some((determination: SpecifyResource<Determination>) =>
    determination.get('isCurrent')
  );

export const businessRuleDefs: MappedBusinessRuleDefs = {
  Address: {
    customInit: (address) => {
      if (address.isNew()) {
        const setPrimary = (): void => {
          address.set('isPrimary', true);
          if (address.collection !== undefined) {
            address.collection.models.forEach(
              (other: SpecifyResource<Address>) => {
                if (other.cid !== address.cid) other.set('isPrimary', false);
              }
            );
          }
        };
        address.on('add', setPrimary);
      }
    },
    fieldChecks: {
      isPrimary: async (address): Promise<BusinessRuleResult> => {
        if (address.get('isPrimary') === true) {
          address.collection?.models.forEach(
            (other: SpecifyResource<Address>) => {
              if (other.cid !== address.cid) {
                other.set('isPrimary', false);
              }
            }
          );
        }
        if (
          address.collection !== undefined &&
          !address.collection?.models.some((c: SpecifyResource<Address>) =>
            c.get('isPrimary')
          )
        ) {
          address.set('isPrimary', true);
        }
        return { isValid: true };
      },
    },
  },
  BorrowMaterial: {
    fieldChecks: {
      quantityReturned: (
        borrowMaterial: SpecifyResource<BorrowMaterial>
      ): void => {
        const returned = borrowMaterial.get('quantityReturned');
        const resolved = borrowMaterial.get('quantityResolved');
        const quantity = borrowMaterial.get('quantity');

        const adjustedReturned =
          typeof quantity === 'number' &&
          typeof returned === 'number' &&
          typeof resolved === 'number'
            ? returned > quantity
              ? quantity
              : returned > resolved
              ? resolved
              : returned
            : undefined;
        if (typeof adjustedReturned === 'number')
          borrowMaterial.set('quantityReturned', adjustedReturned);
      },
      quantityResolved: (
        borrowMaterial: SpecifyResource<BorrowMaterial>
      ): void => {
        const resolved = borrowMaterial.get('quantityResolved');
        const quantity = borrowMaterial.get('quantity');
        const returned = borrowMaterial.get('quantityReturned');

        const adjustedResolved =
          typeof quantity === 'number' &&
          typeof returned === 'number' &&
          typeof resolved === 'number'
            ? resolved > quantity
              ? quantity
              : resolved < returned
              ? returned
              : resolved
            : undefined;

        if (typeof adjustedResolved === 'number')
          borrowMaterial.set('quantityResolved', adjustedResolved);
      },
    },
  },

  CollectionObject: {
    customInit: (collectionObject: SpecifyResource<CollectionObject>): void => {
      const ceField = collectionObject.specifyTable.getField('collectingEvent');
      if (
        ceField?.isDependent() &&
        collectionObject.get('collectingEvent') === undefined
      ) {
        collectionObject.set(
          'collectingEvent',
          new tables.CollectingEvent.Resource()
        );
      }
    },
    fieldChecks: {
      collectionObjectType: (resource) => {
        // Fields ignored for better UX/backend restrictions
        const fieldsToIgnore = [
          'cataloger',
          'catalogNumber',
          'collection',
          'collectionObjectType',
          'version',
        ];

        // Clear all fields of CO except to-many dependents
        resource.specifyTable.fields
          .filter((field) => !f.includes(fieldsToIgnore, field.name))
          .map((field) => {
            const fieldName = field.name as keyof (CollectionObject['fields'] &
              CollectionObject['toManyDependent'] &
              CollectionObject['toManyIndependent'] &
              CollectionObject['toOneDependent'] &
              CollectionObject['toOneIndependent']);
            if (
              !field.isRelationship ||
              !relationshipIsToMany(field) ||
              !field.isDependent()
            )
              resource.set(fieldName, null);
          });

        // Delete all determinations
        const determinations = resource.getDependentResource('determinations');
        while (
          determinations !== undefined &&
          determinations.models.length > 0
        ) {
          determinations.remove(determinations.models[0]);
        }
      },
    },
  },

  Determination: {
    fieldChecks: {
      taxon: async (
        determination: SpecifyResource<Determination>
      ): Promise<BusinessRuleResult | undefined> =>
        determination
          .rgetPromise('taxon', true)
          .then((taxon: SpecifyResource<Taxon> | null) => {
            const getLastAccepted = async (
              taxon: SpecifyResource<Taxon>
            ): Promise<SpecifyResource<Taxon>> =>
              taxon
                .rgetPromise('acceptedTaxon', true)
                .then(async (accepted) =>
                  accepted === null ? taxon : getLastAccepted(accepted)
                );

            const collectionObject = determination.collection?.related;
            if (
              collectionObject !== undefined &&
              collectionObject.specifyTable.name === 'CollectionObject'
            )
              (collectionObject as SpecifyResource<CollectionObject>)
                .rgetPromise('collectionObjectType', true)
                .then((coType: SpecifyResource<CollectionObjectType>) => {
                  /*
                   * Have to set save blockers directly here to get this working.
                   * Since following code has to wait for above rgetPromise to resolve, returning a Promise<BusinessRuleResult> for validation here is too slow and
                   * does not get captured by business rules.
                   */
                  if (
                    coType.get('taxonTreeDef') ===
                    (taxon?.get('definition') ?? '')
                  ) {
                    setSaveBlockers(
                      determination,
                      determination.specifyTable.field.taxon,
                      [],
                      DETERMINATION_TAXON_KEY
                    );
                  } else {
                    setSaveBlockers(
                      determination,
                      determination.specifyTable.field.taxon,
                      [formsText.invalidTree()],
                      DETERMINATION_TAXON_KEY
                    );
                  }
                });

            return taxon === null
              ? {
                  isValid: true,
                  action: () => determination.set('preferredTaxon', null),
                }
              : {
                  isValid: true,
                  action: async () =>
                    determination.set(
                      'preferredTaxon',
                      await getLastAccepted(taxon)
                    ),
                };
          }),
      isCurrent: async (
        determination: SpecifyResource<Determination>
      ): Promise<BusinessRuleResult> => {
        /*
         * Disallow multiple determinations being checked as current
         * Unchecks other determination when one of them gets checked
         */
        if (
          determination.get('isCurrent') &&
          determination.collection !== undefined
        ) {
          determination.collection.models.map(
            (other: SpecifyResource<Determination>) => {
              if (other.cid !== determination.cid) {
                other.set('isCurrent', false);
              }
            }
          );
        }
        // Flag as invalid if no determinations are checked as current
        if (
          determination.collection !== undefined &&
          hasNoCurrentDetermination(determination.collection)
        ) {
          return {
            isValid: false,
            reason: resourcesText.currentDeterminationRequired(),
            saveBlockerKey: CURRENT_DETERMINATION_KEY,
            resource: determination.collection.related,
          };
        }
        return {
          isValid: true,
          saveBlockerKey: CURRENT_DETERMINATION_KEY,
          resource: determination.collection?.related,
        };
      },
    },
    onRemoved: (determination, collection): void => {
      // Block save when no current determinations exist on removing
      if (hasNoCurrentDetermination(collection))
        setSaveBlockers(
          collection.related ?? determination,
          determination.specifyTable.field.isCurrent,
          [resourcesText.currentDeterminationRequired()],
          CURRENT_DETERMINATION_KEY
        );
      // Unblock save when all determinations are removed
      else
        setSaveBlockers(
          collection.related ?? determination,
          determination.specifyTable.field.isCurrent,
          [],
          CURRENT_DETERMINATION_KEY
        );
    },
    onAdded: (determination, collection): void => {
      determination.set('isCurrent', true);
      // Clear any existing save blocker on adding a new current determination
      setSaveBlockers(
        collection.related ?? determination,
        determination.specifyTable.field.isCurrent,
        [],
        CURRENT_DETERMINATION_KEY
      );
    },
  },
  DisposalPreparation: {
    fieldChecks: {
      quantity: checkPrepAvailability,
    },
  },
  DNASequence: {
    fieldChecks: {
      geneSequence: (dnaSequence: SpecifyResource<DNASequence>): void => {
        const current = dnaSequence.get('geneSequence');
        if (current === null) return;
        const countObject = { a: 0, t: 0, g: 0, c: 0, ambiguous: 0 };
        for (let i = 0; i < current.length; i++) {
          const char = current.at(i)?.toLowerCase().trim();
          if (char !== '') {
            switch (char) {
              case 'a': {
                countObject.a += 1;
                break;
              }
              case 't': {
                countObject.t += 1;
                break;
              }
              case 'g': {
                countObject.g += 1;
                break;
              }
              case 'c': {
                countObject.c += 1;
                break;
              }
              default: {
                countObject.ambiguous += 1;
              }
            }
          }
        }
        dnaSequence.set('compA', countObject.a);
        dnaSequence.set('compT', countObject.t);
        dnaSequence.set('compG', countObject.g);
        dnaSequence.set('compC', countObject.c);
        dnaSequence.set('ambiguousResidues', countObject.ambiguous);
        dnaSequence.set(
          'totalResidues',
          countObject.a +
            countObject.t +
            countObject.g +
            countObject.c +
            countObject.ambiguous
        );
      },
    },
  },
  GiftPreparation: {
    fieldChecks: {
      quantity: checkPrepAvailability,
    },
  },
  LoanPreparation: {
    customInit: (resource: SpecifyResource<LoanPreparation>): void => {
      if (!resource.isNew())
        resource.rgetCollection('loanReturnPreparations').then(updateLoanPrep);
    },
    fieldChecks: {
      quantity: checkPrepAvailability,
    },
  },
  LoanReturnPreparation: {
    onRemoved: (
      _loanReturnPrep: SpecifyResource<LoanReturnPreparation>,
      collection: Collection<LoanReturnPreparation>
    ): void => updateLoanPrep(collection),

    customInit: (resource: SpecifyResource<LoanReturnPreparation>): void => {
      const returned = resource.get('quantityReturned');
      const resolved = resource.get('quantityResolved');
      if (returned === undefined) resource.set('quantityReturned', 0);
      if (resolved === undefined) resource.set('quantityResolved', 0);
      if (!resource.isNew()) {
        previousLoanPreparations.previousReturned[resource.cid] =
          Number(returned);
        previousLoanPreparations.previousResolved[resource.cid] =
          Number(resolved);
      }
      updateLoanPrep(resource.collection);
    },
    fieldChecks: {
      quantityReturned: (
        loanReturnPrep: SpecifyResource<LoanReturnPreparation>
      ): void => {
        const returned = Number(loanReturnPrep.get('quantityReturned'))!;
        const previousReturned =
          previousLoanPreparations.previousReturned[loanReturnPrep.cid] ?? 0;
        const previousResolved =
          previousLoanPreparations.previousResolved[loanReturnPrep.cid] ?? 0;

        const totalLoaned = getTotalLoaned(loanReturnPrep)!;

        const totalResolved = getTotalResolved(loanReturnPrep)!;
        const available = totalLoaned - totalResolved;

        if (returned !== previousReturned) {
          if (returned === available && previousReturned - returned === 1) {
          } else if (returned < 0 || previousReturned < 0) {
            loanReturnPrep.set('quantityReturned', 0);
          } else {
            const changeInReturn = returned - previousReturned;
            previousLoanPreparations.previousResolved[loanReturnPrep.cid] =
              changeInReturn + previousResolved;
            loanReturnPrep.set(
              'quantityResolved',
              changeInReturn + previousResolved
            );
          }
        }

        if (returned > totalLoaned)
          loanReturnPrep.set('quantityReturned', totalLoaned);

        const returnedLeft = totalLoaned - getTotalReturned(loanReturnPrep)!;
        if (returned > returnedLeft)
          loanReturnPrep.set('quantityReturned', returnedLeft);

        if (previousResolved < returned) {
          loanReturnPrep.set('quantityResolved', returned);
          previousLoanPreparations.previousResolved[loanReturnPrep.cid] =
            returned;
        }

        previousLoanPreparations.previousReturned[loanReturnPrep.cid] =
          returned;
        updateLoanPrep(loanReturnPrep.collection);
      },
      quantityResolved: (
        loanReturnPrep: SpecifyResource<LoanReturnPreparation>
      ): void => {
        const resolved = Number(loanReturnPrep.get('quantityResolved'));

        const totalLoaned = getTotalLoaned(loanReturnPrep)!;
        const totalResolved = getTotalResolved(loanReturnPrep)!;
        const available = totalLoaned - totalResolved;
        if (resolved > available) {
          loanReturnPrep.set('quantityResolved', available);
        }

        if (resolved < 0) loanReturnPrep.set('quantityResolved', 0);

        previousLoanPreparations.previousResolved[loanReturnPrep.cid] =
          resolved;
        updateLoanPrep(loanReturnPrep.collection);
      },
    },
  },
};
