import React from 'react';

import { DEFAULT_FETCH_LIMIT, fetchCollection } from '../DataModel/collection';
import { f } from '../../utils/functools';
import { sortFunction } from '../../utils/utils';
import type { SpecifyResource } from '../DataModel/legacyTypes';
import { commonText } from '../../localization/common';
import { hasTablePermission } from '../Permissions/helpers';
import type { RA } from '../../utils/types';
import { H3, Ul } from '../Atoms';
import { Link } from '../Atoms/Link';
import { Dialog } from '../Molecules/Dialog';
import { deserializeResource } from '../../hooks/resource';
import { useAsyncState } from '../../hooks/useAsyncState';
import { AnySchema } from '../DataModel/helperTypes';
import { Preparation } from '../DataModel/types';
import { interactionsText } from '../../localization/interactions';
import { schema } from '../DataModel/schema';

function List({
  resources,
  fieldName,
  displayFieldName,
}: {
  readonly resources: RA<SpecifyResource<AnySchema>>;
  readonly fieldName: string;
  readonly displayFieldName: string;
}): JSX.Element {
  const [entries] = useAsyncState(
    React.useCallback(async () => {
      const interactions: RA<SpecifyResource<AnySchema>> = await Promise.all(
        resources.map((resource) => resource.rgetPromise(fieldName))
      );
      return interactions
        .map((resource) => ({
          label: resource.get(displayFieldName),
          href: resource.viewUrl(),
        }))
        .sort(sortFunction(({ label }) => label));
    }, [resources, fieldName, displayFieldName]),
    false
  );

  return resources.length === 0 ? (
    <>{commonText.noResults()}</>
  ) : Array.isArray(entries) ? (
    <Ul>
      {entries.map(({ label, href }, index) => (
        <li key={index}>
          <Link.NewTab href={href}>{label}</Link.NewTab>
        </li>
      ))}
    </Ul>
  ) : (
    <>{commonText.loading()}</>
  );
}

export function ShowLoansCommand({
  preparation,
  onClose: handleClose,
}: {
  readonly preparation: SpecifyResource<Preparation>;
  readonly onClose: () => void;
}): JSX.Element | null {
  const [data] = useAsyncState(
    React.useCallback(
      async () =>
        f.all({
          openLoans: hasTablePermission('LoanPreparation', 'read')
            ? fetchCollection('LoanPreparation', {
                isResolved: false,
                limit: DEFAULT_FETCH_LIMIT,
                preparation: preparation.get('id'),
              }).then(({ records }) => records.map(deserializeResource))
            : undefined,
          resolvedLoans: hasTablePermission('LoanPreparation', 'read')
            ? fetchCollection('LoanPreparation', {
                isResolved: true,
                limit: DEFAULT_FETCH_LIMIT,
                preparation: preparation.get('id'),
              }).then(({ records }) => records.map(deserializeResource))
            : undefined,
          gifts: hasTablePermission('GiftPreparation', 'read')
            ? fetchCollection('GiftPreparation', {
                limit: DEFAULT_FETCH_LIMIT,
                preparation: preparation.get('id'),
              }).then(({ records }) => records.map(deserializeResource))
            : undefined,
          exchanges: hasTablePermission('ExchangeOutPrep', 'read')
            ? fetchCollection('ExchangeOutPrep', {
                limit: DEFAULT_FETCH_LIMIT,
                preparation: preparation.get('id'),
              }).then(({ records }) => records.map(deserializeResource))
            : undefined,
        }),
      [preparation]
    ),
    true
  );

  return typeof data === 'object' ? (
    <Dialog
      buttons={commonText.close()}
      header={commonText.transactions()}
      onClose={handleClose}
    >
      <H3>
        {interactionsText.openLoans({
          loanTable: schema.models.Loan.label,
        })}
      </H3>
      <List
        displayFieldName="loanNumber"
        fieldName="loan"
        resources={data.openLoans ?? []}
      />
      <H3>
        {interactionsText.resolvedLoans({
          loanTable: schema.models.Loan.label,
        })}
      </H3>
      <List
        displayFieldName="loanNumber"
        fieldName="loan"
        resources={data.resolvedLoans ?? []}
      />
      <H3>
        {interactionsText.gifts({
          giftTable: schema.models.Gift.label,
        })}
      </H3>
      <List
        displayFieldName="giftNumber"
        fieldName="gift"
        resources={data.gifts ?? []}
      />
      {Array.isArray(data.exchanges) && data.exchanges.length > 0 && (
        <>
          <H3>
            {interactionsText.exchanges({
              exhangeInTable: schema.models.ExchangeIn.label,
              exhangeOutTable: schema.models.ExchangeOut.label,
            })}
          </H3>
          <List
            displayFieldName="exchangeOutNumber"
            fieldName="exchange"
            resources={data.exchanges}
          />
        </>
      )}
    </Dialog>
  ) : null;
}
