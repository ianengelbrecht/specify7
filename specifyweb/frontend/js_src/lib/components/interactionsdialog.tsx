import React from 'react';
import { useParams } from 'react-router-dom';
import type { State } from 'typesafe-reducer';

import { ajax } from '../ajax';
import { error } from '../assert';
import { fetchCollection } from '../collection';
import type { Disposal, Gift, Loan, RecordSet, Tables } from '../datamodel';
import type { SerializedResource } from '../datamodelutils';
import { f } from '../functools';
import { getBooleanAttribute, getParsedAttribute } from '../helpers';
import { cachableUrl } from '../initialcontext';
import { commonText } from '../localization/common';
import { formsText } from '../localization/forms';
import { getView } from '../parseform';
import { hasPermission, hasTablePermission } from '../permissionutils';
import { formatUrl } from '../querystring';
import { getResourceViewUrl, parseClassName } from '../resource';
import { getModel, schema } from '../schema';
import type { SpecifyModel } from '../specifymodel';
import type { RA } from '../types';
import { defined, filterArray } from '../types';
import { userInformation } from '../userinfo';
import { Link, Ul } from './basic';
import { TableIcon } from './common';
import { ErrorBoundary } from './errorboundary';
import { useAsyncState } from './hooks';
import { icons } from './icons';
import { InteractionDialog } from './interactiondialog';
import { Dialog, dialogClassNames } from './modaldialog';
import { ReportsView } from './reports';
import { OverlayContext } from './router';

export const interactionTables: ReadonlySet<keyof Tables> = new Set<
  keyof Tables
>([
  'Accession',
  'AccessionAgent',
  'AccessionAttachment',
  'AccessionAuthorization',
  'AccessionCitation',
  'Appraisal',
  'Borrow',
  'BorrowAgent',
  'BorrowAttachment',
  'BorrowMaterial',
  'BorrowReturnMaterial',
  'Deaccession',
  'DeaccessionAgent',
  'DeaccessionAttachment',
  'Disposal',
  'DisposalAgent',
  'DisposalAttachment',
  'DisposalPreparation',
  'ExchangeIn',
  'ExchangeInPrep',
  'ExchangeOut',
  'ExchangeOutPrep',
  'Gift',
  'GiftAgent',
  'GiftAttachment',
  'GiftPreparation',
  'InfoRequest',
  'Loan',
  'LoanAgent',
  'LoanAttachment',
  'LoanPreparation',
  'LoanReturnPreparation',
  'Permit',
  'PermitAttachment',
]);

const supportedActions = [
  'NEW_GIFT',
  'NEW_LOAN',
  'RET_LOAN',
  'PRINT_INVOICE',
] as const;

const stringLocalization = {
  RET_LOAN: formsText('returnLoan'),
  PRINT_INVOICE: formsText('printInvoice'),
  LOAN_NO_PRP: formsText('loanWithoutPreparation'),
  'InteractionsTask.LN_NO_PREP': formsText('loanWithoutPreparationDescription'),
  'InteractionsTask.NEW_LN': formsText('createLoan'),
  'InteractionsTask.EDT_LN': formsText('editLoan'),
  'InteractionsTask.NEW_GFT': formsText('createdGift'),
  'InteractionsTask.EDT_GFT': formsText('editGift'),
  'InteractionsTask.CRE_IR': formsText('createInformationRequest'),
  'InteractionsTask.PRT_INV': formsText('printInvoice'),
};

export type InteractionEntry = {
  readonly action: typeof supportedActions[number] | undefined;
  readonly table: keyof Tables;
  readonly label: string | undefined;
  readonly tooltip: string | undefined;
  readonly icon: string | undefined;
};

const url = cachableUrl(
  formatUrl('/context/app.resource', { name: 'InteractionsTaskInit' })
);
const fetchEntries = f.store(
  async (): Promise<RA<InteractionEntry>> =>
    process.env.NODE_ENV === 'test'
      ? []
      : ajax<Element>(url, {
          headers: { Accept: 'application/xml' },
        }).then<RA<InteractionEntry>>(async ({ data }) =>
          Promise.all(
            Array.from(data.querySelectorAll('entry'), async (entry) =>
              f.var(getParsedAttribute(entry, 'action'), async (action) =>
                getBooleanAttribute(entry, 'isOnLeft') ?? false
                  ? ({
                      action: f.includes(supportedActions, action)
                        ? action
                        : undefined,
                      table:
                        action === 'NEW_GIFT'
                          ? 'Gift'
                          : action === 'NEW_LOAN'
                          ? 'Loan'
                          : defined(
                              (await f
                                .maybe(
                                  getParsedAttribute(entry, 'view'),
                                  getView
                                )
                                ?.then((view) =>
                                  typeof view === 'object'
                                    ? (parseClassName(
                                        view.class
                                      ) as keyof Tables)
                                    : undefined
                                )) ??
                                getModel(
                                  getParsedAttribute(entry, 'table') ?? ''
                                )?.name
                            ),
                      label: getParsedAttribute(entry, 'label'),
                      tooltip: getParsedAttribute(entry, 'tooltip'),
                      icon: getParsedAttribute(entry, 'icon'),
                    } as const)
                  : undefined
              )
            )
          ).then(filterArray)
        )
);

function Interactions({
  onClose: handleClose,
  entries,
}: {
  readonly onClose: () => void;
  readonly entries: RA<InteractionEntry>;
}): JSX.Element {
  const [state, setState] = React.useState<
    | State<
        'InteractionState',
        {
          readonly table: 'CollectionObject' | 'Disposal' | 'Gift' | 'Loan';
          readonly actionModel: SpecifyModel<Disposal | Gift | Loan>;
          readonly action: string;
          readonly recordSetsPromise: Promise<{
            readonly records: RA<SerializedResource<RecordSet>>;
            readonly totalCount: number;
          }>;
        }
      >
    | State<'MainState'>
    | State<'ReportsState'>
  >({ type: 'MainState' });
  const handleAction = React.useCallback(
    (action: typeof supportedActions[number], table: keyof Tables): void => {
      if (action === 'PRINT_INVOICE') setState({ type: 'ReportsState' });
      else {
        const isRecordSetAction = action == 'NEW_GIFT' || action == 'NEW_LOAN';
        const model = isRecordSetAction
          ? schema.models.CollectionObject
          : schema.models.Loan;
        setState({
          type: 'InteractionState',
          recordSetsPromise: fetchCollection('RecordSet', {
            specifyUser: userInformation.id,
            type: 0,
            dbTableId: model.tableId,
            domainFilter: true,
            orderBy: '-timestampCreated',
            limit: 5000,
          }),
          table: model.name,
          actionModel:
            table.toLowerCase() === 'loan'
              ? schema.models.Loan
              : table.toLowerCase() === 'gift'
              ? schema.models.Gift
              : table.toLowerCase() === 'gift'
              ? schema.models.Disposal
              : error(`Unknown interaction table: ${table}`),
          action,
        });
      }
    },
    []
  );

  const { action } = useParams();
  React.useEffect(
    () =>
      typeof action === 'string'
        ? f.maybe(
            entries.find((entry) => entry.action === action),
            ({ action, table }) => handleAction(defined(action), table)
          )
        : undefined,
    [action, entries]
  );

  return state.type === 'MainState' ? (
    <Dialog
      buttons={commonText('cancel')}
      className={{
        container: dialogClassNames.narrowContainer,
      }}
      header={commonText('interactions')}
      icon={<span className="text-blue-500">{icons.chat}</span>}
      onClose={handleClose}
    >
      <Ul>
        {entries
          .filter(({ table }) => hasTablePermission(table, 'create'))
          .map(({ label, table, action, tooltip, icon }, index) =>
            action !== 'PRINT_INVOICE' ||
            hasPermission('/report', 'execute') ? (
              <li
                key={index}
                title={
                  typeof tooltip === 'string'
                    ? stringLocalization[
                        tooltip as keyof typeof stringLocalization
                      ] ?? tooltip
                    : undefined
                }
              >
                <Link.Default
                  href={
                    typeof action === 'string'
                      ? `/specify/overlay/interactions/${action}/`
                      : getResourceViewUrl(table)
                  }
                  onClick={
                    typeof action === 'string'
                      ? (event): void => {
                          event.preventDefault();
                          handleAction(action, table);
                        }
                      : undefined
                  }
                >
                  {f.maybe(icon ?? table, (icon) => (
                    <TableIcon label={false} name={icon} />
                  ))}
                  {typeof label === 'string'
                    ? stringLocalization[
                        label as keyof typeof stringLocalization
                      ] ?? label
                    : typeof table === 'string'
                    ? getModel(table)?.label
                    : action}
                </Link.Default>
              </li>
            ) : undefined
          )}
      </Ul>
    </Dialog>
  ) : state.type === 'InteractionState' ? (
    <InteractionDialog
      action={{ model: state.actionModel, name: state.action }}
      model={schema.models[state.table]}
      recordSetsPromise={state.recordSetsPromise}
      searchField={defined(
        defined(getModel(state.table)).getLiteralField(
          state.table === 'Loan'
            ? 'loanNumber'
            : state.table === 'Disposal'
            ? 'disposalNumber'
            : 'catalogNumber'
        )
      )}
      onClose={handleClose}
    />
  ) : state.type === 'ReportsState' ? (
    <ReportsView
      autoSelectSingle
      model={schema.models.Loan}
      resourceId={undefined}
      onClose={handleClose}
    />
  ) : (
    error('Invalid state')
  );
}

export function InteractionsOverlay(): JSX.Element | null {
  const [entries] = useAsyncState(fetchEntries, true);
  const handleClose = React.useContext(OverlayContext);

  return typeof entries === 'object' ? (
    <ErrorBoundary dismissable>
      <Interactions entries={entries} onClose={handleClose} />
    </ErrorBoundary>
  ) : null;
}
