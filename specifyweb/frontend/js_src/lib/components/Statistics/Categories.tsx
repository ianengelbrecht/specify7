import type { CustomStat, DefaultStat, StatLayout, StatsSpec } from './types';
import { H3 } from '../Atoms';
import { Input } from '../Atoms/Form';
import { CustomStatItem, DefaultStatItem } from './StatItems';
import { Button } from '../Atoms/Button';
import { className } from '../Atoms/className';
import { commonText } from '../../localization/common';
import React from 'react';

export function Categories({
  pageLayout,
  statsSpec,
  onAdd: handleAdd,
  onClick: handleClick,
  onRemove: handleRemove,
  onRename: handleRename,
}: {
  readonly pageLayout: StatLayout[number];
  readonly statsSpec: StatsSpec;
  readonly onAdd: ((categoryIndex: number | undefined) => void) | undefined;
  readonly onClick: ((item: CustomStat | DefaultStat) => void) | undefined;
  readonly onRemove:
    | ((categoryIndex: number, itemIndex: number | undefined) => void)
    | undefined;
  readonly onRename:
    | ((newName: string, categoryIndex: number) => void)
    | undefined;
}): JSX.Element {
  return (
    <>
      {pageLayout.categories.map(({ label, items }, categoryIndex) => (
        <div
          className="flex h-auto max-h-80 flex-col content-center gap-2 rounded border-[1px] border-black bg-white p-4"
          key={categoryIndex}
        >
          {handleRename === undefined ? (
            <H3 className="font-bold">{label}</H3>
          ) : (
            <Input.Text
              required
              value={label}
              onValueChange={(newname): void => {
                handleRename(newname, categoryIndex);
              }}
            />
          )}
          <div className="flex-1 overflow-auto pr-4">
            {items?.map((item, itemIndex) =>
              item.type === 'DefaultStat' ? (
                <DefaultStatItem
                  categoryName={item.categoryName}
                  itemName={item.itemName}
                  pageName={item.pageName}
                  key={itemIndex}
                  statsSpec={statsSpec}
                  onClick={
                    typeof handleClick === 'function'
                      ? (): void => {
                          handleClick({
                            type: 'DefaultStat',
                            pageName: item.pageName,
                            categoryName: item.categoryName,
                            itemName: item.itemName,
                          });
                        }
                      : undefined
                  }
                  onRemove={
                    handleRemove === undefined
                      ? undefined
                      : (): void => handleRemove(categoryIndex, itemIndex)
                  }
                />
              ) : (
                <CustomStatItem
                  key={itemIndex}
                  queryId={item.queryId}
                  onClick={
                    typeof handleClick === 'function'
                      ? (): void => {
                          handleClick({
                            type: 'CustomStat',
                            queryId: item.queryId,
                          });
                        }
                      : undefined
                  }
                  onRemove={
                    handleRemove === undefined
                      ? undefined
                      : (): void => handleRemove(categoryIndex, itemIndex)
                  }
                />
              )
            )}
          </div>
          {handleAdd !== undefined && handleRemove !== undefined && (
            <div className="flex gap-2">
              <Button.Small
                variant={className.greenButton}
                onClick={(): void => handleAdd(categoryIndex)}
              >
                {commonText('add')}
              </Button.Small>
              <span className="-ml-2 flex-1" />
              <Button.Small
                variant={className.redButton}
                onClick={(): void => handleRemove(categoryIndex, undefined)}
              >
                {commonText('delete')}
              </Button.Small>
            </div>
          )}
        </div>
      ))}
      {handleAdd !== undefined && (
        <Button.Green
          className="!p-4"
          onClick={(): void => handleAdd(undefined)}
        >
          {commonText('add')}
        </Button.Green>
      )}
    </>
  );
}
