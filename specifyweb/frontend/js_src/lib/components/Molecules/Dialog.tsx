/**
 * React Dialogs
 *
 * @module
 */
import React from 'react';
import Draggable from 'react-draggable';
import type { Props } from 'react-modal';
import Modal from 'react-modal';
import type { LocalizedString } from 'typesafe-i18n';

import { useId } from '../../hooks/useId';
import { listen } from '../../utils/events';
import { KEY } from '../../utils/utils';
import { Button, DialogContext } from '../Atoms/Button';
import { className, dialogIconTriggers } from '../Atoms/className';
import { dialogIcons } from '../Atoms/Icons';
import { LoadingContext } from '../Core/Contexts';
import {
  useHighContrast,
  useReducedTransparency,
  useTransitionDuration,
} from '../UserPreferences/Hooks';
import { usePref } from '../UserPreferences/usePref';
import { useTitle } from './AppTitle';

/**
 * Modal dialog with a loading bar
 * @module
 */
export function LoadingScreen(): null {
  const loading = React.useContext(LoadingContext);
  const resolveRef = React.useRef<() => void>();
  React.useEffect(() => {
    loading(
      new Promise<void>((resolve) => {
        resolveRef.current = resolve;
      })
    );
    return (): void => resolveRef.current?.();
  }, [loading]);

  return null;
}

const commonContainer = 'rounded resize max-w-[90%] shadow-lg shadow-gray-500';
export const dialogClassNames = {
  fullScreen: '!transform-none !w-full !h-full',
  freeContainer: `${commonContainer} max-h-[90%]`,
  narrowContainer: `${commonContainer} max-h-[50%] min-w-[min(20rem,90%)]
    lg:max-w-[50%]`,
  normalContainer: `${commonContainer} max-h-[90%] min-w-[min(30rem,90%)]`,
  wideContainer: `${commonContainer} max-h-[90%] min-w-[min(40rem,90%)]`,
  extraWideContainer: `${commonContainer} max-h-[90%] min-w-[min(20rem,90%)]
    w-[min(60rem,90%)] h-[60rem]`,
  flexContent: 'flex flex-col gap-2',
} as const;

/*
 * Starting at 180 puts dialogs over Handsontable column headers (which have
 * z-index of 180)
 */
const initialIndex = 180;
const topIndex = 10_000;
const dialogIndexes = new Set<number>();
const getNextIndex = (): number =>
  dialogIndexes.size === 0 ? initialIndex : Math.max(...dialogIndexes) + 1;

export const supportsBackdropBlur = globalThis.CSS.supports(
  '((-webkit-backdrop-filter: none) or (backdrop-filter: none))'
);

/**
 * Modal or non-modal dialog. Highly customizable. Used all over the place
 * @remarks
 * Note, if the same components renders a <Dialog>, and on the next render
 * instead renders a different <Dialog> with the same parent, React would
 * reuse the same <Dialog> instance. This means, if content was scrolled down,
 * new dialog, with a different content would already be scrolled down.
 * Possible solution would be to set container.scrollTop=0 on header change,
 * though, that may introduce issues in other places, as same dialogs change
 * header durring lifecycle (ResourceView)
 */
export function Dialog({
  /*
   * Using isOpen prop instead of conditional rendering is optional, but it
   * allows for smooth dialog close animation
   */
  isOpen = true,
  header,
  headerButtons,
  showOrangeBar = false,
  // Default icon type is determined based on dialog button types
  icon: defaultIcon,
  buttons,
  children,
  /*
   * Non-modal dialogs are discouraged due to accessibility concerns and
   * possible state conflicts arising from the user interacting with different
   * parts of the app at the same time
   */
  modal = true,
  onClose: handleClose,
  onResize: handleResize,
  className: {
    // Dialog has optimal width
    container: containerClassName = dialogClassNames.normalContainer,
    // Dialog's content is a flexbox
    content: contentClassName = dialogClassNames.flexContent,
    // Buttons are right-aligned by default
    buttonContainer: buttonContainerClassName = 'justify-end',
    header: headerClassName = `${className.headerPrimary} text-xl`,
  } = {},
  /* Force dialog to stay on top of all others. Useful for exception messages */
  forceToTop = false,
  forwardRef: { content: contentRef, container: externalContainerRef } = {},
}: {
  readonly isOpen?: boolean;
  readonly header: LocalizedString;
  readonly headerButtons?: React.ReactNode;
  readonly showOrangeBar?: boolean;
  /*
   * TEST: review dialogs that don't need icons or dialogs whose autogenerated
   *   icon is incorrect (record view dialog has red icon because of delete
   *   button)
   */
  readonly icon?: JSX.Element | keyof typeof dialogIconTriggers;
  // Have to explicitly pass undefined if you don't want buttons
  readonly buttons: JSX.Element | LocalizedString | undefined;
  readonly children: React.ReactNode;
  readonly modal?: boolean;
  /*
   * Have to explicitly pass undefined if dialog should not be closable
   *
   * This gets called only when dialog is closed by the user.
   * If dialog is removed from the element tree programmatically, callback is
   * not called
   */
  readonly onClose: (() => void) | undefined;
  readonly onResize?: (element: HTMLElement) => void;
  readonly className?: {
    readonly container?: string;
    readonly content?: string;
    readonly buttonContainer?: string;
    readonly header?: string;
  };
  readonly forceToTop?: boolean;
  readonly forwardRef?: {
    readonly content?: React.Ref<HTMLDivElement>;
    readonly container?: React.RefCallback<HTMLDivElement>;
  };
}): JSX.Element {
  const id = useId('modal');

  const [modifyTitle] = usePref('general', 'dialog', 'updatePageTitle');
  useTitle(modal && isOpen && modifyTitle ? header : undefined);

  const reduceTransparency = useReducedTransparency();
  const [transparentDialog] = usePref(
    'general',
    'dialog',
    'transparentBackground'
  );
  const [blurContentBehindDialog] = usePref(
    'general',
    'dialog',
    'blurContentBehindDialog'
  );
  const [showIcon] = usePref('general', 'dialog', 'showIcon');

  const [closeOnEsc] = usePref('general', 'dialog', 'closeOnEsc');
  const [closeOnOutsideClick] = usePref(
    'general',
    'dialog',
    'closeOnOutsideClick'
  );

  /*
   * Don't set index on first render, because that may lead multiple dialogs
   * to have the same index, since render of all children is done before any
   * useEffect can update max z-index)
   */
  const [zIndex, setZindex] = React.useState<number | undefined>(undefined);

  React.useEffect(() => {
    if (!isOpen) return undefined;
    if (forceToTop) {
      setZindex(topIndex);
      return undefined;
    }
    const zIndex = getNextIndex();
    setZindex(zIndex);
    dialogIndexes.add(zIndex);
    return (): void => setZindex(undefined);
  }, [isOpen, forceToTop]);

  React.useEffect(() => {
    if (forceToTop || modal || !isOpen || zIndex === undefined)
      return undefined;

    dialogIndexes.add(zIndex);
    return (): void => void dialogIndexes.delete(zIndex);
  }, [forceToTop, modal, isOpen, zIndex]);

  // Facilitate moving non-modal dialog to top on click
  const [container, setContainer] = React.useState<HTMLDivElement | null>(null);
  const containerRef = React.useRef<HTMLDivElement | null>(null);
  React.useEffect(
    () =>
      forceToTop ||
      modal ||
      !isOpen ||
      zIndex === undefined ||
      container === null
        ? undefined
        : listen(container, 'click', () =>
            // Check if dialog is already at the very top
            Math.max(...dialogIndexes) === zIndex
              ? undefined
              : setZindex(getNextIndex)
          ),
    [forceToTop, modal, isOpen, zIndex, container]
  );

  // Resize listener
  React.useEffect(() => {
    if (
      !isOpen ||
      container === null ||
      handleResize === undefined ||
      globalThis.ResizeObserver === undefined
    )
      return undefined;

    const observer = new globalThis.ResizeObserver(() =>
      handleResize?.(container)
    );
    observer.observe(container);

    return (): void => observer.disconnect();
  }, [isOpen, container, handleResize]);

  const isFullScreen = containerClassName.includes(dialogClassNames.fullScreen);

  const draggableContainer: Props['contentElement'] = React.useCallback(
    (props: React.ComponentPropsWithRef<'div'>, children: React.ReactNode) => (
      <Draggable
        // Don't allow moving the dialog past the window bounds
        bounds="parent"
        // Allow moving the dialog when hovering over the header line
        cancel={`#${id('full-screen')}`}
        // Don't allow moving when in full-screen
        defaultClassName=""
        // Don't need any extra classNames
        defaultClassNameDragged=""
        defaultClassNameDragging=""
        handle={`#${id('handle')}`}
        nodeRef={containerRef}
      >
        <div {...props}>{children}</div>
      </Draggable>
    ),
    [id]
  );

  const [buttonContainer, setButtonContainer] =
    React.useState<HTMLDivElement | null>(null);
  const iconType = React.useMemo(() => {
    if (!showIcon) return 'none';
    if (typeof defaultIcon === 'string') return defaultIcon;
    else if (buttonContainer === null) return 'none';
    /*
     * If icon was not specified explicitly, it is determined based on what
     * matching className dialog buttons have
     */
    return (
      Object.entries(dialogIconTriggers).find(
        ([_type, className]) =>
          className !== '' &&
          typeof buttonContainer.getElementsByClassName(className)[0] ===
            'object'
      )?.[KEY] ?? 'none'
    );
  }, [showIcon, defaultIcon, buttons, buttonContainer]);

  const overlayElement: Props['overlayElement'] = React.useCallback(
    (
      props: React.ComponentPropsWithRef<'div'>,
      contentElement: React.ReactElement
    ) => (
      <div
        {...props}
        onMouseDown={
          closeOnOutsideClick
            ? (event): void => {
                // Outside click detection
                if (
                  modal &&
                  typeof handleClose === 'function' &&
                  event.target === event.currentTarget
                ) {
                  event.preventDefault();
                  handleClose();
                } else props?.onMouseDown?.(event);
              }
            : undefined
        }
      >
        {contentElement}
      </div>
    ),
    [modal, handleClose, closeOnOutsideClick]
  );

  const transitionDuration = useTransitionDuration();
  const highContrast = useHighContrast();

  return (
    <Modal
      aria={{
        labelledby: id('header'),
        describedby: id('content'),
        modal,
      }}
      ariaHideApp={false}
      bodyOpenClassName={null}
      className={`
        flex flex-col gap-2 p-4 outline-none ${containerClassName}
        overflow-x-hidden text-neutral-900 duration-0
        dark:border dark:border-neutral-700 dark:text-neutral-200
        ${modal ? '' : 'pointer-events-auto border border-gray-500'}
        ${
          reduceTransparency || highContrast
            ? 'bg-white dark:bg-neutral-900'
            : (transparentDialog && modal
            ? supportsBackdropBlur
              ? 'bg-white/40 backdrop-blur-lg dark:bg-transparent'
              : 'bg-white/70 dark:bg-black/70'
            : `bg-gradient-to-bl from-gray-200 via-white
                to-white dark:from-neutral-800 dark:via-neutral-900 dark:to-neutral-900`)
        }
      `}
      closeTimeoutMS={transitionDuration === 0 ? undefined : transitionDuration}
      // "overflow-x-hidden" is necessary for the "resize" handle to appear
      contentElement={draggableContainer}
      contentRef={(ref: HTMLDivElement | undefined): void => {
        const container = ref ?? null;
        // Save to state so that React.useEffect hooks are reRun
        setContainer(container);
        // Save to React.useRef so that React Draggable can have immediate access
        containerRef.current = container;
        if (typeof externalContainerRef === 'function')
          externalContainerRef(container);
      }}
      /*
       * Can't use outside click detection that comes with this plugin
       * because of https://github.com/specify/specify7/issues/1248.
       * (it listens on click, not on mouse down)
       */
      htmlOpenClassName={null}
      // Instead, a custom onMouseDown handler is set up for this element
      id={isFullScreen ? id('full-screen') : undefined}
      isOpen={isOpen}
      overlayClassName={{
        base: `w-screen h-screen absolute inset-0 flex items-center
          justify-center opacity-0 ${
            modal
              ? 'bg-gray-500/70 dark:bg-neutral-900/70'
              : 'pointer-events-none'
          } ${blurContentBehindDialog ? 'backdrop-blur' : ''}`,
        afterOpen: 'opacity-100',
        beforeClose: '!opacity-0',
      }}
      overlayElement={overlayElement}
      portalClassName=""
      shouldCloseOnEsc={
        modal && typeof handleClose === 'function' && closeOnEsc
      }
      /*
       * Adding aria-hidden to #root is a legacy solution. Modern solution
       * involves displaying an element with [role="dialog"][aria-modal="true"],
       * which react-modal library already does. See more:
       * https://www.w3.org/WAI/ARIA/apg/example-index/dialog-modal/dialog.html#:~:text=Notes%20on%20aria%2Dmodal%20and%20aria%2Dhidden
       * Additionally, aria-hidden has a drawback of hiding the <h1> element,
       * which causes another accessibility problem.
       */
      shouldCloseOnOverlayClick={false}
      style={{ overlay: { zIndex } }}
      onRequestClose={handleClose}
    >
      {/* "p-4 -m-4" increases the handle size for easier dragging */}
      <span
        className={`
          flex items-center gap-4
          ${isFullScreen ? '' : '-m-4 cursor-move p-4'}
          ${showOrangeBar ? '' : 'flex-wrap'}
        `}
        id={id('handle')}
      >
        <div className="flex items-center gap-2">
          {typeof defaultIcon === 'object' && showIcon
            ? defaultIcon
            : dialogIcons[iconType]}
          <h2 className={headerClassName} id={id('header')}>
            {header}
          </h2>
        </div>
        {headerButtons}
      </span>
      {showOrangeBar && <div className="w-full border-b-2 border-brand-300" />}
      <DialogContext.Provider value={handleClose}>
        {/*
         * "px-1 -mx-1" ensures that focus outline for checkboxes
         * and other inputs is not cut-off. You can also use "px-4 -mx-4" to
         * place container scroll bar at the very edge of the dialog, which
         * looks nice, but is bad UX, because misclics can trigger dialog
         * close
         */}
        <div
          className={`
            -mx-1 flex-1 overflow-y-auto px-1 py-4 text-gray-700
            dark:text-neutral-350 ${contentClassName}
          `}
          id={id('content')}
          ref={contentRef}
        >
          {children}
        </div>
        {buttons !== undefined && (
          <div
            className={`flex gap-2 ${buttonContainerClassName}`}
            ref={setButtonContainer}
          >
            {typeof buttons === 'string' ? (
              // If button was passed directly as text, render it as Blue.Button
              <Button.DialogClose component={Button.Blue}>
                {buttons}
              </Button.DialogClose>
            ) : (
              buttons
            )}
          </div>
        )}
      </DialogContext.Provider>
    </Modal>
  );
}
