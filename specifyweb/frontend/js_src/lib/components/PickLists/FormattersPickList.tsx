import React from 'react';

import { useAsyncState } from '../../hooks/useAsyncState';
import type { RA } from '../../utils/types';
import { resourceOn } from '../DataModel/resource';
import { getModel } from '../DataModel/schema';
import { raise } from '../Errors/Crash';
import type {
  DefaultComboBoxProps,
  PickListItemSimple,
} from '../FormFields/ComboBox';
import { fetchFormatters } from '../Forms/dataObjFormatters';
import { PickListTypes } from './definitions';
import { PickListComboBox } from './index';

export function FormattersPickList(props: DefaultComboBoxProps): JSX.Element {
  const fetchItems = React.useCallback(async () => {
    if (props.resource?.get('type') !== PickListTypes.TABLE) return [];
    const { formatters } = await fetchFormatters;
    const model = getModel(props.resource.get('tableName') ?? '');
    return typeof model === 'object'
      ? formatters
          .filter(({ className }) => className === model.longName)
          .map(({ name, title }) => ({
            value: name ?? title ?? '',
            title: title ?? name ?? '',
          }))
      : [];
  }, [props.resource]);
  const [items, setItems] = useAsyncState<RA<PickListItemSimple>>(
    fetchItems,
    false
  );
  React.useEffect(
    () =>
      props.resource === undefined
        ? undefined
        : resourceOn(
            props.resource,
            'change:tableName change:type',
            (): void => {
              if (props.resource === undefined) return;
              if (props.resource.get('type') !== PickListTypes.TABLE)
                props.resource.set('formatter', null as never);
              fetchItems()
                .then(setItems)
                .catch((error) => {
                  setItems(undefined);
                  raise(error);
                });
            },
            true
          ),
    [props.resource, fetchItems, setItems]
  );

  return (
    <PickListComboBox
      {...props}
      isDisabled={props.isDisabled || items === undefined || items.length === 0}
      items={items}
      pickList={undefined}
      onAdd={undefined}
    />
  );
}
