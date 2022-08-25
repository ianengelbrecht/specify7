/**
 * Generic React Components
 *
 * @module
 *
 */

import React from 'react';
import ReactDOM from 'react-dom';
import { useLocation } from 'react-router-dom';

import type { SortConfigs } from '../cachedefinitions';
import { format } from '../dataobjformatters';
import { f } from '../functools';
import { sortFunction, spanNumber } from '../helpers';
import { getIcon } from '../icons';
import { commonText } from '../localization/common';
import { hasTablePermission } from '../permissionutils';
import { parseResourceUrl } from '../resource';
import { getModel } from '../schema';
import type { RA } from '../types';
import { defined } from '../types';
import { Button, className, Link, Textarea } from './basic';
import { softFail } from './errorboundary';
import { copyTextToClipboard } from './filepicker';
import { useAsyncState, useBooleanState, useTitle } from './hooks';
import { icons } from './icons';
import { usePref } from './preferenceshooks';
import { useCachedState } from './statecache';

const MAX_HUE = 360;

/**
 * Convert first 2 characters of a table name to a number [0,255] corresponding
 * to color hue.
 *
 * Used for autogenerated table icons if table icon image is missing.
 */
const getHue = spanNumber(
  // eslint-disable-next-line unicorn/prefer-code-point
  'a'.charCodeAt(0) * 2,
  // eslint-disable-next-line unicorn/prefer-code-point
  'z'.charCodeAt(0) * 2,
  0,
  MAX_HUE
);

/** Generate an HSL color based on the first 2 characters of a string */
export const stringToColor = (name: string): string =>
  f.var(
    name.toLowerCase(),
    (name) =>
      `hsl(${getHue(
        // eslint-disable-next-line unicorn/prefer-code-point
        (name[0] ?? 'a').charCodeAt(0) + (name[1] ?? 'a').charCodeAt(0)
      )}, 70%, 50%)`
  );

/**
 * Renders a table icon or autogenerates a new one
 */
export function TableIcon({
  name,
  label,
  /**
   * It is highly recommended to use the same icon size everywhere, as that
   * improves consistency, thus, this should be overwritten only if it is
   * strictly necessary.
   */
  className = 'w-table-icon h-table-icon flex-shrink-0',
}: {
  readonly name: string;
  /**
   * Set this to false only if icon would be rendered adjacent to the table name.
   * In all other cases, set this to true, or explicitly set the label as a
   * string
   */
  readonly label: boolean | string;
  readonly className?: string;
}): JSX.Element {
  const tableIconSource = getIcon(name);
  const resolvedTableLabel =
    label === false
      ? undefined
      : typeof label === 'string'
      ? label
      : getModel(name)?.label ?? '';
  const role = typeof resolvedTableLabel === 'string' ? 'img' : undefined;
  const ariaHidden = resolvedTableLabel === undefined;
  if (typeof tableIconSource === 'string')
    return (
      <span
        aria-hidden={ariaHidden}
        aria-label={typeof role === 'string' ? resolvedTableLabel : undefined}
        className={`${className} bg-contain bg-center bg-no-repeat`}
        role={role}
        style={{ backgroundImage: `url('${tableIconSource}')` }}
        title={resolvedTableLabel}
      />
    );

  // If icon is missing, show an autogenerated one:
  return (
    <span
      aria-hidden={ariaHidden}
      aria-label={resolvedTableLabel}
      className={`
        flex h-table-icon w-table-icon items-center justify-center
        rounded-sm text-sm text-white
      `}
      role={role}
      style={{ backgroundColor: stringToColor(name) }}
      title={resolvedTableLabel}
    >
      {name.slice(0, 2).toUpperCase()}
    </span>
  );
}

export const tableIconUndefined = (
  <span
    aria-label={commonText('unmapped')}
    className={`
      flex h-table-icon w-table-icon items-center justify-center font-bold
      text-red-600
    `}
    role="img"
  >
    {icons.ban}
  </span>
);

export const tableIconSelected = (
  <span
    aria-label={commonText('mapped')}
    className={`
      flex h-table-icon w-table-icon items-center justify-center font-bold
      text-green-500
    `}
    role="img"
  >
    {icons.check}
  </span>
);

export const tableIconEmpty = (
  <span aria-hidden className="h-table-icon w-table-icon" />
);

export type SortConfig<FIELD_NAMES extends string> = {
  readonly sortField: FIELD_NAMES;
  readonly ascending: boolean;
};

export function SortIndicator<FIELD_NAMES extends string>({
  fieldName,
  sortConfig,
}: {
  readonly fieldName: string;
  readonly sortConfig: SortConfig<FIELD_NAMES> | undefined;
}): JSX.Element {
  const isSorted = sortConfig?.sortField === fieldName;
  return (
    <span className="text-brand-300">
      {isSorted && (
        <span className="sr-only">
          {sortConfig.ascending
            ? commonText('ascending')
            : commonText('descending')}
        </span>
      )}
      {isSorted
        ? sortConfig.ascending
          ? icons.chevronUp
          : icons.chevronDown
        : undefined}
    </span>
  );
}

export function useSortConfig<NAME extends keyof SortConfigs>(
  cacheKey: NAME,
  defaultField: SortConfigs[NAME],
  ascending = true
): readonly [
  sortConfig: SortConfig<SortConfigs[NAME]>,
  handleSort: (fieldName: SortConfigs[NAME]) => void,
  applySortConfig: <T>(
    array: RA<T>,
    mapper: (item: T) => boolean | number | string | null | undefined
  ) => RA<T>
] {
  const [sortConfig = { sortField: defaultField, ascending }, setSortConfig] =
    useCachedState('sortConfig', cacheKey);
  const handleClick = React.useCallback(
    (sortField: SortConfigs[NAME]) => {
      const newSortConfig: SortConfig<SortConfigs[NAME]> = {
        sortField,
        ascending:
          sortField === sortConfig?.sortField ? !sortConfig.ascending : true,
      };
      (
        setSortConfig as (
          sortConfig: SortConfig<SortConfigs[NAME]> | undefined
        ) => void
      )(newSortConfig);
    },
    [sortConfig, setSortConfig]
  );
  const applySortConfig = React.useCallback(
    <T,>(
      array: RA<T>,
      mapper: (item: T) => boolean | number | string | null | undefined
    ): RA<T> =>
      sortConfig === undefined
        ? array
        : Array.from(array).sort(sortFunction(mapper, !sortConfig.ascending)),
    [sortConfig]
  );
  return [sortConfig, handleClick, applySortConfig];
}

/**
 * A React Portal wrapper
 *
 * @remarks
 * Based on https://blog.logrocket.com/learn-react-portals-by-example/
 *
 * Used when an elements needs to be renreded outside of the bounds of
 * the container that has overflow:hidden
 */
export function Portal({
  children,
}: {
  readonly children: JSX.Element;
}): JSX.Element {
  const element = React.useMemo(() => document.createElement('div'), []);

  React.useEffect(() => {
    const portalRoot = document.getElementById('portal-root');
    if (portalRoot === null) throw new Error('Portal root was not found');
    portalRoot.append(element);
    return (): void => element.remove();
  }, [element]);

  return ReactDOM.createPortal(children, element);
}

export function AppTitle({
  title,
  type,
}: {
  readonly title: string;
  readonly type?: 'form';
}): null {
  const [updateTitle] = usePref('form', 'behavior', 'updatePageTitle');
  useTitle(type !== 'form' || updateTitle ? title : undefined);
  return null;
}

export function AutoGrowTextArea({
  containerClassName,
  ...props
}: Parameters<typeof Textarea>[0] & {
  readonly containerClassName?: string;
}): JSX.Element {
  const [textArea, setTextArea] = React.useState<HTMLTextAreaElement | null>(
    null
  );
  const [shadow, setShadow] = React.useState<HTMLDivElement | null>(null);
  /*
   * If user manually resized the textarea, need to keep the shadow in sync
   * Fixes https://github.com/specify/specify7/issues/1783
   * Can't simply convert auto growing textarea into a regular one on the fly
   * because that interrupts the resize operation
   */
  React.useEffect(() => {
    if (
      textArea === null ||
      shadow === null ||
      globalThis.ResizeObserver === undefined
    )
      return undefined;
    const observer = new globalThis.ResizeObserver(() => {
      shadow.style.height = textArea.style.height;
      shadow.style.width = textArea.style.width;
    });
    observer.observe(textArea);
    return (): void => observer.disconnect();
  }, [textArea, shadow]);

  React.useEffect(() => {
    if (typeof props.forwardRef === 'function') props.forwardRef(textArea);
    else if (
      typeof props.forwardRef === 'object' &&
      props.forwardRef !== null &&
      'current' in props.forwardRef
    )
      /* REFACTOR: improve typing to make this editable */
      // @ts-expect-error Modifying a read-only property
      props.forwardRef.current = textArea;
  }, [textArea, props.forwardRef]);
  return (
    <div
      className={`
        relative min-h-[calc(theme(spacing.7)*var(--rows))] overflow-hidden
        ${containerClassName ?? ''}
      `}
      style={{ '--rows': props.rows ?? 3 } as React.CSSProperties}
    >
      {/*
       * Shadow a textarea with a div, allowing it to autoGrow. Source:
       * https://css-tricks.com/the-cleanest-trick-for-autogrowing-textareas/
       */}
      <div
        className={`
          textarea-shadow invisible whitespace-pre-wrap [grid-area:1/1/2/2]
          print:hidden ${className.textArea}
        `}
        ref={setShadow}
      >
        {`${props.value?.toString() ?? ''} `}
      </div>
      <Textarea
        {...props}
        className={`
          absolute top-0 h-full [grid-area:1/1/2/2]
          ${props.className ?? ''}
        `}
        forwardRef={setTextArea}
      />
    </div>
  );
}

const copyMessageTimeout = 3000;

export function CopyButton({
  text,
  label = commonText('copyToClipboard'),
}: {
  readonly text: string;
  readonly label?: string;
}): JSX.Element {
  const [wasCopied, handleCopied, handleNotCopied] = useBooleanState();
  return (
    <Button.Green
      className="whitespace-nowrap"
      onClick={(): void =>
        void copyTextToClipboard(text).then((): void => {
          handleCopied();
          globalThis.setTimeout(handleNotCopied, copyMessageTimeout);
        })
      }
    >
      {wasCopied ? commonText('copied') : label}
    </Button.Green>
  );
}

export function FormattedResource({
  resourceUrl,
  fallback = commonText('loading'),
}: {
  readonly resourceUrl: string;
  readonly fallback?: string;
}): JSX.Element | null {
  const resource = React.useMemo(() => {
    const [tableName, id] = defined(parseResourceUrl(resourceUrl));
    const model = defined(getModel(tableName));
    return new model.Resource({ id });
  }, [resourceUrl]);
  const [formatted] = useAsyncState(
    React.useCallback(async () => format(resource).catch(softFail), [resource]),
    false
  );
  return typeof resource === 'object' &&
    hasTablePermission(resource.specifyModel.name, 'read') ? (
    <Link.Default href={resource.viewUrl()}>
      {formatted ?? fallback}
    </Link.Default>
  ) : (
    <>{formatted ?? fallback}</>
  );
}

export const loadingGif = (
  <div className="hover:animate-hue-rotate [.reduce-motion_&]:animate-hue-rotate">
    <div
      className={`
        spinner-border h-20 w-20 rounded-full border-8 border-brand-300
        [.motion-normal_&]:animate-spin
        [.motion-normal_&]:border-r-transparent
      `}
      role="status"
    >
      <span className="sr-only">{commonText('loading')}</span>
    </div>
  </div>
);

/** Based on react-router's <NavLink> */
export function ActiveLink<T extends Parameters<typeof Link.Default>[0]>({
  component: LinkComponent = Link.Default,
  'aria-current': ariaCurrent = 'page',
  end = false,
  ...props
}: T & {
  readonly end?: boolean;
  readonly component?: (props: T) => JSX.Element;
}): JSX.Element {
  const location = useLocation();
  const isActive =
    location.pathname === props.href ||
    `${location.pathname}${location.hash}` === props.href ||
    location.hash === props.href ||
    (!end &&
      location.pathname.startsWith(props.href) &&
      location.pathname.charAt(props.href.length) === '/');
  return (
    <LinkComponent
      {...(props as T)}
      aria-current={isActive ? ariaCurrent : undefined}
    />
  );
}
