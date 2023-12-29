/*!
  * Bootstrap v5.3.0 (https://getbootstrap.com/)
  * Copyright 2011-2023 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.bootstrap = factory());
})(this, (function () { 'use strict';

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/data.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  /**
   * Constants
   */

  const elementMap = new Map();
  const Data = {
    set(element, key, instance) {
      if (!elementMap.has(element)) {
        elementMap.set(element, new Map());
      }
      const instanceMap = elementMap.get(element);

      // make it clear we only want one instance per element
      // can be removed later when multiple key/instances are fine to be used
      if (!instanceMap.has(key) && instanceMap.size !== 0) {
        // eslint-disable-next-line no-console
        console.error(`Bootstrap doesn't allow more than one instance per element. Bound instance: ${Array.from(instanceMap.keys())[0]}.`);
        return;
      }
      instanceMap.set(key, instance);
    },
    get(element, key) {
      if (elementMap.has(element)) {
        return elementMap.get(element).get(key) || null;
      }
      return null;
    },
    remove(element, key) {
      if (!elementMap.has(element)) {
        return;
      }
      const instanceMap = elementMap.get(element);
      instanceMap.delete(key);

      // free up element references if there are no instances left for an element
      if (instanceMap.size === 0) {
        elementMap.delete(element);
      }
    }
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/index.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const MAX_UID = 1000000;
  const MILLISECONDS_MULTIPLIER = 1000;
  const TRANSITION_END = 'transitionend';

  /**
   * Properly escape IDs selectors to handle weird IDs
   * @param {string} selector
   * @returns {string}
   */
  const parseSelector = selector => {
    if (selector && window.CSS && window.CSS.escape) {
      // document.querySelector needs escaping to handle IDs (html5+) containing for instance /
      selector = selector.replace(/#([^\s"#']+)/g, (match, id) => `#${CSS.escape(id)}`);
    }
    return selector;
  };

  // Shout-out Angus Croll (https://goo.gl/pxwQGp)
/**
* @description This function takes an object as an argument and returns its type
* (string) based on its value. If the object is null or undefined; it will return
* just that. Otherwise it will try to determine the objects type by comparing its
* prototype property using a regular expression pattern.
* 
* @param { object } object - The `object` input parameter is passed as an argument
* to the function and serves as the object whose type is to be determined.
* 
* @returns { object } This function takes an object as input and returns its type
* as a string. It first checks if the input is null or undefined and returns "null"
* or "undefined" accordingly. If the input is not null nor undefined (i.e., it's an
* actual object), the function calls Object.prototype.toString() on it and extracts
* the type of the object from the resulting string using a regular expression. The
* returned type is then lowercased and returned as a string.
* 
* In other words: if the input is null/undefined (i.e., not an actual object), the
* function simply returns "null" or "undefined". If it's an actual object though...
*/
  const toType = object => {
    if (object === null || object === undefined) {
      return `${object}`;
    }
    return Object.prototype.toString.call(object).match(/\s([a-z]+)/i)[1].toLowerCase();
  };

  /**
   * Public Util API
   */

  const getUID = prefix => {
    do {
      prefix += Math.floor(Math.random() * MAX_UID);
    } while (document.getElementById(prefix));
    return prefix;
  };
/**
* @description This function calculates the total transition duration of an element
* by retrieving the `transition-duration` and `transition-delay` properties from the
* element's computed styles and concatenating them into a single duration value.
* 
* @param {  } element - The `element` input parameter is the DOM element for which
* the transition duration is being retrieved.
* 
* @returns { number } This function takes an HTML element as input and returns the
* transition duration of that element. It first checks if the element exists and
* then retrieves the "transition-duration" and "transition-delay" styles from the
* element using window.getComputedStyle(). If both values are not found or are not
* numeric numbers without commas and spaces trimmed then return 0 as output.
*/
  const getTransitionDurationFromElement = element => {
    if (!element) {
      return 0;
    }

    // Get transition-duration of the element
    let {
      transitionDuration,
      transitionDelay
    } = window.getComputedStyle(element);
    const floatTransitionDuration = Number.parseFloat(transitionDuration);
    const floatTransitionDelay = Number.parseFloat(transitionDelay);

    // Return 0 if element or transition duration is not found
    if (!floatTransitionDuration && !floatTransitionDelay) {
      return 0;
    }

    // If multiple durations are defined, take the first
    transitionDuration = transitionDuration.split(',')[0];
    transitionDelay = transitionDelay.split(',')[0];
    return (Number.parseFloat(transitionDuration) + Number.parseFloat(transitionDelay)) * MILLISECONDS_MULTIPLIER;
  };
/**
* @description This function dispatches an event named TRANSITION_END to the element
* passed as an argument when the transition end event is triggered.
* 
* @param {  } element - The `element` input parameter is the DOM element for which
* the transition end event should be triggered.
* 
* @returns { any } This function creates a new `Event` object with the name
* `TRANSITION_END` and dispatches it on the `element`.
*/
  const triggerTransitionEnd = element => {
    element.dispatchEvent(new Event(TRANSITION_END));
  };
/**
* @description This function isElement($1) checks whether a given object is an HTML
* element. It does this by checking if the object is an object and if it has a
* nodeType property.
* 
* @param { object } object - The `object` input parameter is an arbitrary Object or
* DOM element to be checked whether it has a `nodeType` property.
* 
* @returns { boolean } The output returned by this function is a boolean value
* indicating whether a given object is an element or not. If the object is falsy
* (e.g., `undefined` or not an object), the function returns `false`. If the object
* is an object with a `jquery` property (likely from a jQuery object), the function
* reduces it to its underlying element and checks if it has a `nodeType` property;
* if it does not have one or is not an object at all (i.e., it's neither an element
* nor a document object), it returns `false`.
*/
  const isElement$1 = object => {
    if (!object || typeof object !== 'object') {
      return false;
    }
    if (typeof object.jquery !== 'undefined') {
      object = object[0];
    }
    return typeof object.nodeType !== 'undefined';
  };
/**
* @description This function takes an `object` and returns the underlying DOM
* element(s) associated with it. It first checks if `object` is a jQuery object or
* a Node element.
* 
* @param { object } object - The `object` input parameter is the value that the
* function should operate on.
* 
* @returns {  } The `getElement` function takes an `object` and returns the following:
* 
* 1/ If `object` is a jQuery object or a DOM element:
* 		- If `object.jquery` is true (i.e., it's a jQuery object), the function returns
* the underlying DOM element (via `object[0]`).
* 		- Otherwise (if it's a plain DOM element), the function returns the element itself.
* 2/ If `object` is a string and contains more than one selector (separated by space):
* 		- The function calls `parseSelector()` on the string to parse it into a selector
* expression.
* 		- It then uses `document.querySelector()` to select the first matching element
* using that expression.
* 3/ If `object` is not any of the above:
* 		- The function returns `null`.
* 
* So the output of the `getElement` function depends on the type of input passed to
* it.
*/
  const getElement = object => {
    // it's a jQuery object or a node element
    if (isElement$1(object)) {
      return object.jquery ? object[0] : object;
    }
    if (typeof object === 'string' && object.length > 0) {
      return document.querySelector(parseSelector(object));
    }
    return null;
  };
/**
* @description The given function is an IIFE (Immediately Invoked Function Expression)
* that takes a parameter `element` and returns a boolean value indicating whether
* the specified element is visible or not. It checks if the element exists and has
* any client rects before checking the `visibility` property of the element using
* `getComputedStyle()` method. If the `details` element is closed and its content
* appears falsely visible when it should be closed based on the visibility status
* of the detail's text (the summay of which may not be explicitly shown), the function
* also checks for the existence and relationship of the parent `summary` element to
* ensure that it isn't the `details` element.
* 
* @param { object } element - The `element` input parameter is the element to be
* checked for visibility.
* 
* @returns { boolean } The output returned by this function is a boolean value
* indicating whether an Element is visible or not.
*/
  const isVisible = element => {
    if (!isElement$1(element) || element.getClientRects().length === 0) {
      return false;
    }
    const elementIsVisible = getComputedStyle(element).getPropertyValue('visibility') === 'visible';
    // Handle `details` element as its content may falsie appear visible when it is closed
    const closedDetails = element.closest('details:not([open])');
    if (!closedDetails) {
      return elementIsVisible;
    }
    if (closedDetails !== element) {
      const summary = element.closest('summary');
      if (summary && summary.parentNode !== closedDetails) {
        return false;
      }
      if (summary === null) {
        return false;
      }
    }
    return elementIsVisible;
  };
/**
* @description This function checks whether an Element object is disabled or not by
* checking for several possible indicators of disability:
* 
* 	- `nodeType` property
* 	- `classList.contains('disabled')` method
* 	- `disabled` attribute
* 	- `hasAttribute('disabled')` method with the value !== 'false'
* 
* @param { any } element - The `element` input parameter is not used or modified
* within the function.
* 
* @returns { boolean } The function `isDisabled` takes an HTML element as input and
* returns a boolean value indicating whether the element is disabled or not.
*/
  const isDisabled = element => {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) {
      return true;
    }
    if (element.classList.contains('disabled')) {
      return true;
    }
    if (typeof element.disabled !== 'undefined') {
      return element.disabled;
    }
    return element.hasAttribute('disabled') && element.getAttribute('disabled') !== 'false';
  };
/**
* @description This function finds the ShadowRoot of a given element. If the element
* doesn't have a ShadowRoot or is the root of the document itself (i.e., no shadow
* root at all), it returns null.
* 
* @param {  } element - The `element` input parameter is used to search for a shadow
* root associated with the given element.
* 
* @returns { object } This function takes an HTML element as an argument and returns
* the ShadowRoot element associated with that element if one exists. If no ShadowRoot
* is found then it returns null.
* 
* Here's a step-by-step breakdown of what the function does:
* 
* 1/ Checks if the document has support for Shadow DOM by checking the existence of
* the `attachShadow` method on the `Document` object. If there's no support for
* Shadow DOM then it returns null directly.
* 2/ Checks if the given element has a `getRootNode` method.
*/
  const findShadowRoot = element => {
    if (!document.documentElement.attachShadow) {
      return null;
    }

    // Can find the shadow root otherwise it'll return the document
    if (typeof element.getRootNode === 'function') {
      const root = element.getRootNode();
      return root instanceof ShadowRoot ? root : null;
    }
    if (element instanceof ShadowRoot) {
      return element;
    }

    // when we don't find a shadow root
    if (!element.parentNode) {
      return null;
    }
    return findShadowRoot(element.parentNode);
  };
/**
* @description The `noop` function does nothing and returns immediately.
* 
* @returns {  } The `noop` function has no return statement and returns `undefined`,
* which is the default value when a function does not explicitly return a value.
*/
  const noop = () => {};

  /**
   * Trick to restart an element's animation
   *
   * @param {HTMLElement} element
   * @return void
   *
   * @see https://www.charistheo.io/blog/2021/02/restart-a-css-animation-with-javascript/#restarting-a-css-animation
   */
  const reflow = element => {
    element.offsetHeight; // eslint-disable-line no-unused-expressions
  };

/**
* @description This function checks if jQuery is defined and returns it if it is
* defined and the `data-bs-no-jquery` attribute is not present on the document body.
* 
* @returns {  } The output returned by this function is `null`.
* 
* The function checks if `window.jQuery` exists and if the `data-bs-no-jquery`
* attribute is not present on the `body` element. If both conditions are true (i.e.,
* `window.jQuery` exists and the `data-bs-no-jquery` attribute is not present), the
* function returns `window.jQuery`.
*/
  const getjQuery = () => {
    if (window.jQuery && !document.body.hasAttribute('data-bs-no-jquery')) {
      return window.jQuery;
    }
    return null;
  };
  const DOMContentLoadedCallbacks = [];
/**
* @description This function adds an event listener to the `DOMContentLoaded` event
* on the `document` object and queues up any provided callback functions to be called
* when the document is ready.
* 
* @param {  } callback - The `callback` input parameter is passed to the `DOMContentLoaded`
* event listener function when the `onDOMContentLoaded` function is called.
* 
* @returns { any } This function takes a single argument `callback`, which is a
* function that will be called when the document is ready. If the document is currently
* still loading (`document.readyState` is "loading"), the function adds an event
* listener to listen for the `DOMContentLoaded` event. When the event is triggered
* (i.e., when the document is fully loaded), the function calls all of the callbacks
* that have been added to `DOMContentLoadedCallbacks`.
*/
  const onDOMContentLoaded = callback => {
    if (document.readyState === 'loading') {
      // add listener on the first call when the document is in loading state
      if (!DOMContentLoadedCallbacks.length) {
        document.addEventListener('DOMContentLoaded', () => {
          for (const callback of DOMContentLoadedCallbacks) {
            callback();
          }
        });
      }
      DOMContentLoadedCallbacks.push(callback);
    } else {
      callback();
    }
  };
/**
* @description This function returns a boolean value indicating whether the document
* is written from right to left (RTL) or not.
* 
* @returns { boolean } The function `isRTL` returns a boolean value indicating whether
* the directionality of the document is right-to-left (RTL) or not. It does so by
* checking the `dir` attribute of the `documentElement` element.
* 
* If the `dir` attribute is set to "rtl", then the function returns `true`.
*/
  const isRTL = () => document.documentElement.dir === 'rtl';
/**
* @description This function defines a jQuery plugin by providing an object with
* several methods and properties.
* 
* @param { object } plugin - The `plugin` input parameter is used to pass an object
* with properties such as `NAME`, `jQueryInterface`, and possibly others depending
* on the plugin implementation.
* 
* @returns {  } The output of this function is an object that has a `jQueryInterface`
* method and a `noConflict` method. The ` jQueryInterface` method is a function that
* can be called on a jQuery-enabled element to trigger the functionality of the plugin.
*/
  const defineJQueryPlugin = plugin => {
    onDOMContentLoaded(() => {
      const $ = getjQuery();
      /* istanbul ignore if */
      if ($) {
        const name = plugin.NAME;
        const JQUERY_NO_CONFLICT = $.fn[name];
        $.fn[name] = plugin.jQueryInterface;
        $.fn[name].Constructor = plugin;
        $.fn[name].noConflict = () => {
          $.fn[name] = JQUERY_NO_CONFLICT;
          return plugin.jQueryInterface;
        };
      }
    });
  };
/**
* @description This function takes a potential callback function and executes it
* with any given arguments.
* 
* @param {  } possibleCallback - The `possibleCallback` input parameter is a function
* that can be provided as an optional argument to the `execute` function. If a
* function is provided at this position and it is not null or undefined (i.e., if
* `typeof possibleCallback === 'function'` evaluates to true), the function will be
* called with the `args` parameter and its return value will be returned by the
* `execute` function.
* 
* @param { object } args - The `args` input parameter is an optional array of arguments
* that will be passed to the callback function (if one is provided).
* 
* @param { any } defaultValue - The `defaultValue` input parameter provides a default
* value to return if the `possibleCallback` argument is not a function.
* 
* @returns {  } The output returned by this function is the value returned by the
* provided callback function (if it is a function) or the defaultValue if the provided
* callback is not a function.
*/
  const execute = (possibleCallback, args = [], defaultValue = possibleCallback) => {
    return typeof possibleCallback === 'function' ? possibleCallback(...args) : defaultValue;
  };
/**
* @description This function adds an event listener to a transition element and
* executes a provided callback function after the transition ends. If the transition
* ends within a certain time period (added by `durationPadding`), the function
* immediately executes the callback.
* 
* @param {  } callback - The `callback` parameter is a function that will be called
* after the transition ends (i.e., when the animation is complete) with `target` as
* the element that triggered the transition end event.
* 
* @param {  } transitionElement - The `transitionElement` input parameter passed to
* the `executeAfterTransition` function refers to the element that is undergoing a
* transition.
* 
* @param { boolean } waitForTransition - The `waitForTransition` input parameter
* determines whether the function should wait for the transition to complete before
* executing the provided callback function. If set to `true`, the function will wait
* for the transition end event before executing the callback.
* 
* @returns {  } This function takes a `callback`, `transitionElement`, and an optional
* `waitForTransition` parameter. It returns nothing (i.e., no value) but triggers a
* callback function after the transition ends. The function first sets up an event
* listener on the `transitionElement` to listen for the `TRANSITION_END` event. It
* then uses `setTimeout` to delay triggering the `callback` function by the duration
* of the transition (as determined by `getTransitionDurationFromElement()`) plus a
* small padding value. If the transition ends before the timeout expires (i.e., the
* `called` flag is set to `true`), the `callback` function is executed immediately.
*/
  const executeAfterTransition = (callback, transitionElement, waitForTransition = true) => {
    if (!waitForTransition) {
      execute(callback);
      return;
    }
    const durationPadding = 5;
    const emulatedDuration = getTransitionDurationFromElement(transitionElement) + durationPadding;
    let called = false;
/**
* @description This function is a IIFE (Immediately Invoked Function Expression)
* that sets up an event listener for the `transitionend` event on an element. It
* checks if the target element of the transition is the same as the element being
* listened to. If they are not the same elements it does nothing.
* 
* @returns {  } This function takes an argument `transitionElement` and a callback
* `callback`. It returns nothing (i.e., "undefined").
*/
    const handler = ({
      target
    }) => {
      if (target !== transitionElement) {
        return;
      }
      called = true;
      transitionElement.removeEventListener(TRANSITION_END, handler);
      execute(callback);
    };
    transitionElement.addEventListener(TRANSITION_END, handler);
    setTimeout(() => {
      if (!called) {
        triggerTransitionEnd(transitionElement);
      }
    }, emulatedDuration);
  };

  /**
   * Return the previous/next element of a list.
   *
   * @param {array} list    The list of elements
   * @param activeElement   The active element
   * @param shouldGetNext   Choose to get next or previous element
   * @param isCycleAllowed
   * @return {Element|elem} The proper element
   */
  const getNextActiveElement = (list, activeElement, shouldGetNext, isCycleAllowed) => {
    const listLength = list.length;
    let index = list.indexOf(activeElement);

    // if the element does not exist in the list return an element
    // depending on the direction and if cycle is allowed
    if (index === -1) {
      return !shouldGetNext && isCycleAllowed ? list[listLength - 1] : list[0];
    }
    index += shouldGetNext ? 1 : -1;
    if (isCycleAllowed) {
      index = (index + listLength) % listLength;
    }
    return list[Math.max(0, Math.min(index, listLength - 1))];
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/event-handler.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const namespaceRegex = /[^.]*(?=\..*)\.|.*/;
  const stripNameRegex = /\..*/;
  const stripUidRegex = /::\d+$/;
  const eventRegistry = {}; // Events storage
  let uidEvent = 1;
  const customEvents = {
    mouseenter: 'mouseover',
    mouseleave: 'mouseout'
  };
  const nativeEvents = new Set(['click', 'dblclick', 'mouseup', 'mousedown', 'contextmenu', 'mousewheel', 'DOMMouseScroll', 'mouseover', 'mouseout', 'mousemove', 'selectstart', 'selectend', 'keydown', 'keypress', 'keyup', 'orientationchange', 'touchstart', 'touchmove', 'touchend', 'touchcancel', 'pointerdown', 'pointermove', 'pointerup', 'pointerleave', 'pointercancel', 'gesturestart', 'gesturechange', 'gestureend', 'focus', 'blur', 'change', 'reset', 'select', 'submit', 'focusin', 'focusout', 'load', 'unload', 'beforeunload', 'resize', 'move', 'DOMContentLoaded', 'readystatechange', 'error', 'abort', 'scroll']);

  /**
   * Private methods
   */

  function makeEventUid(element, uid) {
    return uid && `${uid}::${uidEvent++}` || element.uidEvent || uidEvent++;
  }
/**
* @description The given function `getElementsEvents` returns the collection of
* events associated with a given HTML element.
* 
* @param { object } element - The `element` input parameter passed to the function
* `getElementEvents()` is used as a reference to an HTML element object from which
* the function retrieves the event listeners and stores them inside the `eventRegistry`
* object.
* 
* @returns { object } The function `getElementEvents(element)` returns an object
* containing events registered on the specified element.
*/
  function getElementEvents(element) {
    const uid = makeEventUid(element);
    element.uidEvent = uid;
    eventRegistry[uid] = eventRegistry[uid] || {};
    return eventRegistry[uid];
  }
/**
* @description This function is a factory for creating EventHandlers that can be
* used to attach an event listener to an element.
* 
* @param { object } element - The `element` input parameter specifies the DOM element
* to which the event handler is attached.
* 
* @param {  } fn - The `fn` parameter is a function reference that represents the
* click handler to be attached to the element.
* 
* @returns {  } The `bootstrapHandler` function returns a new function that is a
* wrapper around the provided `fn` function. This new function handles event delegation
* and one-off event attachment. In other words:
* 
* 	- It calls the `hydrateObj` function with the event and an options object that
* includes `delegateTarget: element`. This attaches the event handler to the nearest
* parent element that matches the selector specified by the `event.target`.
* 	- If the `oneOff` flag is set (i.e., if the function was called with `handler.oneOff
* = true`), it removes the original event listener after it has been called. This
* prevents the event from being triggered multiple times when the same element is
* clicked or touched.
* 	- It applies the original `fn` function to the event.
* 
* In other words: the output of this function is a new function that attaches an
* event listener to an element and calls the original function with the event object.
*/
  function bootstrapHandler(element, fn) {
    return function handler(event) {
      hydrateObj(event, {
        delegateTarget: element
      });
      if (handler.oneOff) {
        EventHandler.off(element, event.type, fn);
      }
      return fn.apply(element, [event]);
    };
  }
/**
* @description This function is a bootstrap delegation handler that handles events
* delegated from an element to its descendants.
* 
* @param {  } element - The `element` parameter is used as the root element to find
* child elements matching the specified selector.
* 
* @param { string } selector - The `selector` input parameter is a string that selects
* the descendants of the `element` to which the event handler should be applied.
* 
* @param {  } fn - The `fn` parameter is a function that represents the click handler
* that should be called when an event delegation occurs.
* 
* @returns {  } This function returns a handler function that listens for events on
* the `element` parameter and delegates them to all elements matching the `selector`
* parameter. If an event is triggered on one of these matched elements (`target`),
* the `fn` parameter is called with the original event object as an argument.
*/
  function bootstrapDelegationHandler(element, selector, fn) {
    return function handler(event) {
      const domElements = element.querySelectorAll(selector);
      for (let {
        target
      } = event; target && target !== this; target = target.parentNode) {
        for (const domElement of domElements) {
          if (domElement !== target) {
            continue;
          }
          hydrateObj(event, {
            delegateTarget: target
          });
          if (handler.oneOff) {
            EventHandler.off(element, event.type, selector, fn);
          }
          return fn.apply(target, [event]);
        }
      }
    };
  }
/**
* @description This function finds an event object within an objects' values that
* matches a given callable and delegation selector (if provided).
* 
* @param { object } events - The `events` parameter is an object that contains a
* collection of events.
* 
* @param {  } callable - The `callable` input parameter specifies the function to
* be invoked for the event.
* 
* @param { string } delegationSelector - The `delegationSelector` parameter specifies
* a selector to filter out events that have already been delegated to another handler.
* 
* @returns { object } The output of the function `findHandler` is a single event
* object from the `events` object that has the following properties:
* 
* 	- `callable` equal to the provided `callable` parameter
* 	- `delegationSelector` equal to the provided `delegationSelector` parameter (if
* it was provided) or `null` if no delegation selector was provided.
* 
* In other words., the function returns the first event object that matches both
* criteria from the `events` object.
*/
  function findHandler(events, callable, delegationSelector = null) {
    return Object.values(events).find(event => event.callable === callable && event.delegationSelector === delegationSelector);
  }
/**
* @description This function takes an `originalTypeEvent`, a `handler` function (or
* a string), and a `delegationFunction`, and normalizes them into an array of three
* elements:
* 
* 1/ A flag indicating if the handler is delegated (a string) or not (`true` or `false`).
* 2/ The original handler function or the delegation function to be called.
* 3/ The type event that should be fired.
* 
* It returns this normalized array.
* 
* @param { string } originalTypeEvent - The `originalTypeEvent` input parameter is
* the initial value of the `type` property of the Event object that triggered the
* event handler.
* 
* @param { string } handler - The `handler` parameter is used to specify a JavaScript
* function that will be called when the event occurs. If the `handler` parameter is
* a string containing a selector (e.g. "#myelement"), it specifies a delegate handler
* and the function returned by the delegation function will be called.
* 
* @param {  } delegationFunction - The `delegationFunction` parameter is a function
* that is used to determine whether the event handler is delegated or not. If the
* `handler` parameter is a string (i.e., a selector), then the event handler is
* considered to be delegated.
* 
* @returns { array } The function `normalizeParameters` takes three arguments:
* `originalTypeEvent`, `handler`, and `delegationFunction`.
*/
  function normalizeParameters(originalTypeEvent, handler, delegationFunction) {
    const isDelegated = typeof handler === 'string';
    // TODO: tooltip passes `false` instead of selector, so we need to check
    const callable = isDelegated ? delegationFunction : handler || delegationFunction;
    let typeEvent = getTypeEvent(originalTypeEvent);
    if (!nativeEvents.has(typeEvent)) {
      typeEvent = originalTypeEvent;
    }
    return [isDelegated, callable, typeEvent];
  }
/**
* @description This function adds an event handler to an HTML element. It normalizes
* the parameters passed and separates delegated and non-delegated handlers.
* 
* @param {  } element - The `element` parameter passed into `addHandler()` is a DOM
* element to which the event handler will be attached.
* 
* @param { string } originalTypeEvent - The `originalTypeEvent` parameter passes
* through a string that represents the original type event to be handled (such as
* "mouseover" or "click"), unaltered and without the namespace.
* 
* @param {  } handler - The `handler` input parameter passed to the `addHandler()`
* function is the actual callback function that will be triggered when the event occurs.
* 
* @param {  } delegationFunction - The `delegationFunction` input parameter is used
* to specify a function that will be called when the event is delegated to a child
* element.
* 
* @param { boolean } oneOff - The `oneOff` parameter indicates whether the event
* handler should be executed only once or every time the event is triggered.
* 
* @returns { object } The `addHandler` function takes five parameters: `element`,
* `originalTypeEvent`, `handler`, `delegationFunction`, and `oneOff`. It returns
* nothing; instead it adds an event listener to the `element` with the provided
* `handler` function and specifications for event delegation and one-off execution.
* The return value of the function is not defined.
*/
  function addHandler(element, originalTypeEvent, handler, delegationFunction, oneOff) {
    if (typeof originalTypeEvent !== 'string' || !element) {
      return;
    }
    let [isDelegated, callable, typeEvent] = normalizeParameters(originalTypeEvent, handler, delegationFunction);

    // in case of mouseenter or mouseleave wrap the handler within a function that checks for its DOM position
    // this prevents the handler from being dispatched the same way as mouseover or mouseout does
    if (originalTypeEvent in customEvents) {
/**
* @description This function wraps a provided function `fn` and modifies its behavior
* for event delegation.
* 
* @param {  } fn - The `fn` input parameter is the function that should be wrapped
* with the additional condition.
* 
* @returns {  } The given function `wrapFunction` takes a function `fn` as an input
* and returns a new function that wraps the original function with a condition. The
* output returned by this function is the wrapped function `fn` with an added condition.
* 
* In simple terms:
* 
* The function `wrapFunction` will only call the original function `fn` if the event's
* related target is not the delegate target or the delegate target does not contain
* the related target. If the condition is met (i.e., the related target is not the
* delegate target or the delegate target does not contain the related target), the
* wrapped function will return the result of calling the original function with the
* event object as an argument.
*/
      const wrapFunction = fn => {
        return function (event) {
          if (!event.relatedTarget || event.relatedTarget !== event.delegateTarget && !event.delegateTarget.contains(event.relatedTarget)) {
            return fn.call(this, event);
          }
        };
      };
      callable = wrapFunction(callable);
    }
    const events = getElementEvents(element);
    const handlers = events[typeEvent] || (events[typeEvent] = {});
    const previousFunction = findHandler(handlers, callable, isDelegated ? handler : null);
    if (previousFunction) {
      previousFunction.oneOff = previousFunction.oneOff && oneOff;
      return;
    }
    const uid = makeEventUid(callable, originalTypeEvent.replace(namespaceRegex, ''));
    const fn = isDelegated ? bootstrapDelegationHandler(element, handler, callable) : bootstrapHandler(element, callable);
    fn.delegationSelector = isDelegated ? handler : null;
    fn.callable = callable;
    fn.oneOff = oneOff;
    fn.uidEvent = uid;
    handlers[uid] = fn;
    element.addEventListener(typeEvent, fn, isDelegated);
  }
/**
* @description This function removes a handler (i.e., a function) for a specific
* event type (e.g., "click") on an HTML element.
* 
* @param {  } element - The `element` input parameter is the DOM element to which
* the event handler is attached and from which the event listener needs to be removed.
* 
* @param { object } events - The `events` parameter is an object that contains a
* collection of event listeners for the element.
* 
* @param { string } typeEvent - The `typeEvent` input parameter specifies the type
* of event to remove a handler for.
* 
* @param {  } handler - The `handler` input parameter is the handler function that
* should be removed from the event listener.
* 
* @param { string } delegationSelector - The `delegationSelector` input parameter
* specifies a selector to use for event delegation.
* 
* @returns { any } The `removeHandler` function takes several parameters and returns
* no value (it is a void function).
*/
  function removeHandler(element, events, typeEvent, handler, delegationSelector) {
    const fn = findHandler(events[typeEvent], handler, delegationSelector);
    if (!fn) {
      return;
    }
    element.removeEventListener(typeEvent, fn, Boolean(delegationSelector));
    delete events[typeEvent][fn.uidEvent];
  }
/**
* @description This function removes event handlers that have a specific namespace
* from an element and its event listeners.
* 
* @param {  } element - The `element` parameter is passed as an argument to the
* function and it refers to the DOM element on which the event listeners are registered.
* 
* @param { object } events - The `events` input parameter is an object that stores
* a collection of events that have been registered on an element.
* 
* @param { string } typeEvent - The `typeEvent` parameter passed into the
* `removeNamespacedHandlers()` function specifies the type of event that should be
* filtered for handlers with a matching namespace.
* 
* @param { string } namespace - The `namespace` input parameter specifies a portion
* of the event handler name that needs to be removed from the hander key before
* checking if it matches the existing handler.
* 
* @returns { object } The output of the function `removeNamespacedHandlers` is an
* array of events that have been removed from the element's event listener collection.
* The function takes four arguments: `element`, `events`, `typeEvent`, and `namespace`.
* 
* The function loops through the events associated with the specified `typeEvent`
* and filters out those that have a namespace that matches the specified `namespace`.
* It then removes the filtered events from the element's event listener collection
* using the `removeHandler` function.
*/
  function removeNamespacedHandlers(element, events, typeEvent, namespace) {
    const storeElementEvent = events[typeEvent] || {};
    for (const [handlerKey, event] of Object.entries(storeElementEvent)) {
      if (handlerKey.includes(namespace)) {
        removeHandler(element, events, typeEvent, event.callable, event.delegationSelector);
      }
    }
  }
/**
* @description This function takes a JavaScript event object as an argument and
* returns the native event type (e.g. "click", "mousemove", etc.) from a namespaced
* event string (e.g. "click.bs.button"). It does this by removing the namespace
* portion of the event string using a regular expression and then checking if the
* resulting event string is recognized as a custom event. If it is not recognized
* as a custom event (i.e.
* 
* @param {  } event - The `event` input parameter is the actual browser event object
* passed from an element's Event Listener.
* 
* @returns { string } The output returned by this function is the event type string
* without the namespace prefix. For example:
* 
* 	- If the input event is `click.bs.button`, the function will return `click`.
* 	- If the input event is `customEvent.namespace`, the function will return `customEvent`.
* 
* In other words.
*/
  function getTypeEvent(event) {
    // allow to get the native events from namespaced events ('click.bs.button' --> 'click')
    event = event.replace(stripNameRegex, '');
    return customEvents[event] || event;
  }
  const EventHandler = {
    on(element, event, handler, delegationFunction) {
      addHandler(element, event, handler, delegationFunction, false);
    },
    one(element, event, handler, delegationFunction) {
      addHandler(element, event, handler, delegationFunction, true);
    },
    off(element, originalTypeEvent, handler, delegationFunction) {
      if (typeof originalTypeEvent !== 'string' || !element) {
        return;
      }
      const [isDelegated, callable, typeEvent] = normalizeParameters(originalTypeEvent, handler, delegationFunction);
      const inNamespace = typeEvent !== originalTypeEvent;
      const events = getElementEvents(element);
      const storeElementEvent = events[typeEvent] || {};
      const isNamespace = originalTypeEvent.startsWith('.');
      if (typeof callable !== 'undefined') {
        // Simplest case: handler is passed, remove that listener ONLY.
        if (!Object.keys(storeElementEvent).length) {
          return;
        }
        removeHandler(element, events, typeEvent, callable, isDelegated ? handler : null);
        return;
      }
      if (isNamespace) {
        for (const elementEvent of Object.keys(events)) {
          removeNamespacedHandlers(element, events, elementEvent, originalTypeEvent.slice(1));
        }
      }
      for (const [keyHandlers, event] of Object.entries(storeElementEvent)) {
        const handlerKey = keyHandlers.replace(stripUidRegex, '');
        if (!inNamespace || originalTypeEvent.includes(handlerKey)) {
          removeHandler(element, events, typeEvent, event.callable, event.delegationSelector);
        }
      }
    },
    trigger(element, event, args) {
      if (typeof event !== 'string' || !element) {
        return null;
      }
      const $ = getjQuery();
      const typeEvent = getTypeEvent(event);
      const inNamespace = event !== typeEvent;
      let jQueryEvent = null;
      let bubbles = true;
      let nativeDispatch = true;
      let defaultPrevented = false;
      if (inNamespace && $) {
        jQueryEvent = $.Event(event, args);
        $(element).trigger(jQueryEvent);
        bubbles = !jQueryEvent.isPropagationStopped();
        nativeDispatch = !jQueryEvent.isImmediatePropagationStopped();
        defaultPrevented = jQueryEvent.isDefaultPrevented();
      }
      const evt = hydrateObj(new Event(event, {
        bubbles,
        cancelable: true
      }), args);
      if (defaultPrevented) {
        evt.preventDefault();
      }
      if (nativeDispatch) {
        element.dispatchEvent(evt);
      }
      if (evt.defaultPrevented && jQueryEvent) {
        jQueryEvent.preventDefault();
      }
      return evt;
    }
  };
/**
* @description This function takes an object `obj` and a optional `meta` object as
* input and returns the original `obj` object with any property found missing or
* undefined filled-in from the `meta` object using Object.defineProperty().
* 
* @param { object } obj - The `obj` input parameter is the object that will be
* modified by the function.
* 
* @param { object } meta - The `meta` parameter is an optional object that contains
* properties to be added to the `obj` object.
* 
* @returns { object } This function takes an object `obj` and an optional `meta`
* object as input. It mutates `obj` by setting its properties to the values from
* `meta`, if the property already exists on `obj`, it sets the value using
* Object.defineProperty() to make the property configurable and return a getter that
* returns the value from `meta`. Otherwise it overrides the existing property.
* 
* The function returns `obj` after mutating it.
*/
  function hydrateObj(obj, meta = {}) {
    for (const [key, value] of Object.entries(meta)) {
      try {
        obj[key] = value;
      } catch (_unused) {
        Object.defineProperty(obj, key, {
          configurable: true,
          get() {
            return value;
          }
        });
      }
    }
    return obj;
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/manipulator.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  function normalizeData(value) {
    if (value === 'true') {
      return true;
    }
    if (value === 'false') {
      return false;
    }
    if (value === Number(value).toString()) {
      return Number(value);
    }
    if (value === '' || value === 'null') {
      return null;
    }
    if (typeof value !== 'string') {
      return value;
    }
    try {
      return JSON.parse(decodeURIComponent(value));
    } catch (_unused) {
      return value;
    }
  }
/**
* @description This function takes a string key as input and returns a normalized
* version of the key by replacing all capital letters with dashes and lowercase equivalent.
* 
* @param { string } key - The `key` input parameter is a string that receives the
* original data key to be normalized.
* 
* @returns { string } The function takes a string key as input and replaces all
* characters that are not lowercase letters with an underscore and the corresponding
* lowercase letter.
* 
* The output is a new string where all characters are now lowercase letters and all
* non-letter characters have been replaced by an underscore.
*/
  function normalizeDataKey(key) {
    return key.replace(/[A-Z]/g, chr => `-${chr.toLowerCase()}`);
  }
  const Manipulator = {
    setDataAttribute(element, key, value) {
      element.setAttribute(`data-bs-${normalizeDataKey(key)}`, value);
    },
    removeDataAttribute(element, key) {
      element.removeAttribute(`data-bs-${normalizeDataKey(key)}`);
    },
    getDataAttributes(element) {
      if (!element) {
        return {};
      }
      const attributes = {};
      const bsKeys = Object.keys(element.dataset).filter(key => key.startsWith('bs') && !key.startsWith('bsConfig'));
      for (const key of bsKeys) {
        let pureKey = key.replace(/^bs/, '');
        pureKey = pureKey.charAt(0).toLowerCase() + pureKey.slice(1, pureKey.length);
        attributes[pureKey] = normalizeData(element.dataset[key]);
      }
      return attributes;
    },
    getDataAttribute(element, key) {
      return normalizeData(element.getAttribute(`data-bs-${normalizeDataKey(key)}`));
    }
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/config.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Class definition
   */

  class Config {
    // Getters
/**
* @description This function is a `static` method that returns an empty object `{}`.
* 
* @returns { object } The output of the function is an object literatireal `{}`.
*/
    static get Default() {
      return {};
    }
/**
* @description This function returns an empty object literal (`{}`).
* 
* @returns { object } The output of this function is an empty object `{}`.
*/
    static get DefaultType() {
      return {};
    }
/**
* @description This function throws an error because it is a static method that
* expects to be implemented by the developer with the name of a component (e.g.,
* `getName()`) and there is no implementation provided.
* 
* @returns { any } The function does not return any output as it throws an error.
* The `getName()` method is defined as a static method and it is not implemented.
* Therefore the line `throw new Error('You have to implement the static method "NAME",
* for each component');` is executed when the function is called.
*/
    static get NAME() {
      throw new Error('You have to implement the static method "NAME", for each component!');
    }
/**
* @description This function `_getConfig` is responsible for:
* 
* 1/ Merging the provided `config` object with a pre-defined configuration object
* using `this._mergeConfigObj`.
* 2/ Performing some additional processing on the merged config object using `this._configAfterMerge`.
* 3/ Type-checking the config object to ensure it meets certain criteria.
* 4/ Returning the processed and type-checked config object.
* 
* @param { object } config - The `config` input parameter is merged with a predefined
* configuration object and then type-checked before being returned.
* 
* @returns { object } Based on the code snippet provided:
* 
* The ` `_getConfig()` function takes a `config` parameter and performs the following
* operations:
* 
* 1/ Merges the given `config` object with a default configuration object using the
* `_mergeConfigObj()` method.
* 2/ Applies any additional configuration changes using the `_configAfterMerge()` method.
* 3/ Performs type checking on the resulting `config` object using the `_typeCheckConfig()`
* method.
* 
* Finally , the function returns the `config` object after all of these operations
* have been applied.
*/
    _getConfig(config) {
      config = this._mergeConfigObj(config);
      config = this._configAfterMerge(config);
      this._typeCheckConfig(config);
      return config;
    }
/**
* @description This function simply returns the input `config` object unchanged.
* 
* @param { object } config - The `config` input parameter is not used within the
* functionbody of `_configAfterMerge`.
* 
* @returns { object } The function `_configAfterMerge` takes a configuration object
* `config` as an argument and returns the same configuration object without making
* any changes.
*/
    _configAfterMerge(config) {
      return config;
    }
/**
* @description This function `_mergeConfigObj` takes a `config` object and an `element`
* object (or a string), and merges multiple configuration objects together into a
* new object.
* 
* @param {  } config - The `config` input parameter allows for merging of any provided
* configuration object with the default configuration and the configuration obtained
* from data- attributes on the element.
* 
* @param { object } element - The `element` input parameter is used to provide
* additional configuration attributes from a DOM element's data- attributes or
* attribute values.
* 
* @returns { object } The output returned by this function is an object that combines
* the properties of multiple sources:
* 
* 1/ `this.constructor.Default`: The default configuration object for the constructor
* (not specified here)
* 2/ `jsonConfig`: A configuration object parsed from a JSON data attribute on the
* `element` parameter (if present and valid JSON)
* 3/ `Manipulator.getDataAttributes(element)`: An object containing all data attributes
* of the `element` parameter (except for the JSON data attribute already processed)
* 4/ `config`: An optional configuration object passed as a argument to the function
* (if present and not undefined)
* 
* The function returns an object with the properties of all these sources merged together.
*/
    _mergeConfigObj(config, element) {
      const jsonConfig = isElement$1(element) ? Manipulator.getDataAttribute(element, 'config') : {}; // try to parse

      return {
        ...this.constructor.Default,
        ...(typeof jsonConfig === 'object' ? jsonConfig : {}),
        ...(isElement$1(element) ? Manipulator.getDataAttributes(element) : {}),
        ...(typeof config === 'object' ? config : {})
      };
    }
/**
* @description This function checks that the types of properties within an object
* config match the expected types defined by the constructor's `DefaultType` property.
* It does this by looping over the object's properties and comparing the value type
* to the expected type using a RegExp test.
* 
* @param { object } config - The `config` input parameter is the object containing
* the configuration options that need to be verified for valid types.
* 
* @param { object } configTypes - The `configTypes` parameter is an object with a
* set of expected types for each property defined inside the `config` parameter
* passed to the function.
* 
* @returns { object } This function takes a `config` object and a default type
* configuration map `configTypes`, and checks that each property of the `config`
* object matches the expected type specified on the same property. It returns undefined
* if all properties pass the type check.
*/
    _typeCheckConfig(config, configTypes = this.constructor.DefaultType) {
      for (const [property, expectedTypes] of Object.entries(configTypes)) {
        const value = config[property];
        const valueType = isElement$1(value) ? 'element' : toType(value);
        if (!new RegExp(expectedTypes).test(valueType)) {
          throw new TypeError(`${this.constructor.NAME.toUpperCase()}: Option "${property}" provided type "${valueType}" but expected type "${expectedTypes}".`);
        }
      }
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap base-component.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const VERSION = '5.3.0';

  /**
   * Class definition
   */

  class BaseComponent extends Config {
/**
* @description This is a constructor function for an object that initialize elements
* with a specific configuration. It takes two arguments:
* 
* 	- `element` - the DOM element to be configured
* 	- `config` - the configuration object for the element
* 
* The function first calls the superclass constructor (i.e. the one defined before
* this one) and then checks if the `element` argument is valid by using the
* `getElement()` method. If the element is not found it returns without doing anything.
* 
* Otherwise it sets `this._element` to the validated element and `this._config` to
* the config object.
* 
* @param { object } element - The `element` input parameter is used to specify the
* DOM element that this instance of the constructor should be associated with.
* 
* @param { object } config - The `config` input parameter provides configuration
* options for the instance of the constructor.
* 
* @returns { object } The function takes two arguments: `element` and `config`. It
* first calls `super()`, which does nothing since the function doesn't extend any
* other function. Then it gets the `element` argument and checks if it's a valid DOM
* element. If it's not a valid element returns. If it is a valid element sets
* `this._element` to that element and gets the config object and sets `this._config`
* to it. Finally it sets `Data.set(this._element(), this.constructor.DATA_KEY.,
* this);` which sets a private data key on the element with value 'this'.
*/
    constructor(element, config) {
      super();
      element = getElement(element);
      if (!element) {
        return;
      }
      this._element = element;
      this._config = this._getConfig(config);
      Data.set(this._element, this.constructor.DATA_KEY, this);
    }

    // Public
/**
* @description This function disposdisposes of an object instance by:
* 
* 	- removing it from the Data hash map
* 	- unbinding event listeners
* 	- setting all properties to null
* 
* @returns {  } The `dispose` function clears all data and event handlers associated
* with an instance of an object.
*/
    dispose() {
      Data.remove(this._element, this.constructor.DATA_KEY);
      EventHandler.off(this._element, this.constructor.EVENT_KEY);
      for (const propertyName of Object.getOwnPropertyNames(this)) {
        this[propertyName] = null;
      }
    }
/**
* @description This function schedules a callback function to be executed after the
* current transition (if any) and also takes into account if the animation should
* be ran or not.
* 
* @param {  } callback - The `callback` parameter is a function that will be executed
* after the transition (if any) has completed.
* 
* @param { object } element - The `element` input parameter passes a specific DOM
* element to be animated to the `executeAfterTransition()` function inside the queue
* callback.
* 
* @param { boolean } isAnimated - The `isAnimated` input parameter of `_queueCallback()`
* indicates whether the transition is animated or not.
* 
* @returns {  } The ` queueCallback` function does not return any value or output.
*/
    _queueCallback(callback, element, isAnimated = true) {
      executeAfterTransition(callback, element, isAnimated);
    }
/**
* @description This function _getConfig merges configuration objects and performs
* type checking before returning the finalized config.
* 
* @param { object } config - The `config` input parameter is merged with existing
* config object and then processed further before being returned.
* 
* @returns { object } The function `_getConfig` returns the `config` object after
* it has been merged with the default configuration for the element and then type-checked.
*/
    _getConfig(config) {
      config = this._mergeConfigObj(config, this._element);
      config = this._configAfterMerge(config);
      this._typeCheckConfig(config);
      return config;
    }

    // Static
/**
* @description This function retrieves a single instance of an object that is
* associated with the specified DOM element.
* 
* @param { any } element - The `element` input parameter is used to retrieve the
* underlying DOM element associated with the instance of the object being retrieved.
* 
* @returns { object } The output of the `getInstance` function is `undefined`.
* 
* The function attempts to retrieve a stored instance of an object using `Data.get()`
* method with the `getElement()` method as the key and `this.DATA_KEY` as the cache
* key.
*/
    static getInstance(element) {
      return Data.get(getElement(element), this.DATA_KEY);
    }
/**
* @description This function returns an instance of a class (parameterized by "this")
* either from the cache or creates a new one if no existing instance is found for
* the given element and configuration.
* 
* @param {  } element - The `element` input parameter is used to specify the target
* element for which an instance of the class should be created or retrieved from cache.
* 
* @param { object } config - The `config` input parameter is an object that provides
* additional configuration options for the constructor of the class being invoked.
* 
* @returns {  } The output of the given function `getOrCreateInstance` is an instance
* of the class `this`.
* 
* If there is already an instance associated with the specified `element`, the
* function returns that instance. Otherwise (i.e., if no instance exists), a new
* instance is created using the `new` keyword and the element and config arguments
* are passed to the constructor.
*/
    static getOrCreateInstance(element, config = {}) {
      return this.getInstance(element) || new this(element, typeof config === 'object' ? config : null);
    }
/**
* @description This function simply returns the value of the constant `VERSION`.
* 
* @returns { string } The output of the function `VERSION` is `undefined`.
*/
    static get VERSION() {
      return VERSION;
    }
/**
* @description This function defines a static property named `DATA_KEY` that returns
* a string concatenation of `bs.`, followed by the value of the instance property `NAME`.
* 
* @returns { string } The function `get DATA_KEY()` returns a string that concatenates
* the substring "bs." with the current ` NAME` property of the object.
* 
* The output would be a string like "bs.NAME".
*/
    static get DATA_KEY() {
      return `bs.${this.NAME}`;
    }
/**
* @description This function defines a static method `EVENT_KEY` that returns a
* string literal `.${this.DATA_KEY}`.
* 
* @returns { string } This function is defining a static method called `EVENT_KEY`
* on the object.
*/
    static get EVENT_KEY() {
      return `.${this.DATA_KEY}`;
    }
/**
* @description The function `eventName` takes a `name` argument and returns an string
* with the format `<name>${this.EVENT_KEY}`.
* 
* @param { string } name - The `name` input parameter passes a string value that
* gets concatenated with a constant string(`${this.EVENT_KEY}`) to create the final
* event name that is returned by the function.
* 
* @returns { string } The function `eventName()` returns a string by concatenating
* the input name parameter with a constant event key (`${this.EVENT_KEY}`) to create
* a unique event name.
* 
* For example:
* 
* 	- If `name` is "click", then `eventName("click")` returns `"clickMYEVENTKEY"`.
* 
* The output is a string that includes the input name and a unique event key suffix.
*/
    static eventName(name) {
      return `${name}${this.EVENT_KEY}`;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/selector-engine.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const getSelector = element => {
    let selector = element.getAttribute('data-bs-target');
    if (!selector || selector === '#') {
      let hrefAttribute = element.getAttribute('href');

      // The only valid content that could double as a selector are IDs or classes,
      // so everything starting with `#` or `.`. If a "real" URL is used as the selector,
      // `document.querySelector` will rightfully complain it is invalid.
      // See https://github.com/twbs/bootstrap/issues/32273
      if (!hrefAttribute || !hrefAttribute.includes('#') && !hrefAttribute.startsWith('.')) {
        return null;
      }

      // Just in case some CMS puts out a full URL with the anchor appended
      if (hrefAttribute.includes('#') && !hrefAttribute.startsWith('#')) {
        hrefAttribute = `#${hrefAttribute.split('#')[1]}`;
      }
      selector = hrefAttribute && hrefAttribute !== '#' ? hrefAttribute.trim() : null;
    }
    return parseSelector(selector);
  };
  const SelectorEngine = {
    find(selector, element = document.documentElement) {
      return [].concat(...Element.prototype.querySelectorAll.call(element, selector));
    },
    findOne(selector, element = document.documentElement) {
      return Element.prototype.querySelector.call(element, selector);
    },
    children(element, selector) {
      return [].concat(...element.children).filter(child => child.matches(selector));
    },
    parents(element, selector) {
      const parents = [];
      let ancestor = element.parentNode.closest(selector);
      while (ancestor) {
        parents.push(ancestor);
        ancestor = ancestor.parentNode.closest(selector);
      }
      return parents;
    },
    prev(element, selector) {
      let previous = element.previousElementSibling;
      while (previous) {
        if (previous.matches(selector)) {
          return [previous];
        }
        previous = previous.previousElementSibling;
      }
      return [];
    },
    // TODO: this is now unused; remove later along with prev()
    next(element, selector) {
      let next = element.nextElementSibling;
      while (next) {
        if (next.matches(selector)) {
          return [next];
        }
        next = next.nextElementSibling;
      }
      return [];
    },
    focusableChildren(element) {
      const focusables = ['a', 'button', 'input', 'textarea', 'select', 'details', '[tabindex]', '[contenteditable="true"]'].map(selector => `${selector}:not([tabindex^="-"])`).join(',');
      return this.find(focusables, element).filter(el => !isDisabled(el) && isVisible(el));
    },
    getSelectorFromElement(element) {
      const selector = getSelector(element);
      if (selector) {
        return SelectorEngine.findOne(selector) ? selector : null;
      }
      return null;
    },
    getElementFromSelector(element) {
      const selector = getSelector(element);
      return selector ? SelectorEngine.findOne(selector) : null;
    },
    getMultipleElementsFromSelector(element) {
      const selector = getSelector(element);
      return selector ? SelectorEngine.find(selector) : [];
    }
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/component-functions.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const enableDismissTrigger = (component, method = 'hide') => {
    const clickEvent = `click.dismiss${component.EVENT_KEY}`;
    const name = component.NAME;
    EventHandler.on(document, clickEvent, `[data-bs-dismiss="${name}"]`, function (event) {
      if (['A', 'AREA'].includes(this.tagName)) {
        event.preventDefault();
      }
      if (isDisabled(this)) {
        return;
      }
      const target = SelectorEngine.getElementFromSelector(this) || this.closest(`.${name}`);
      const instance = component.getOrCreateInstance(target);

      // Method argument is left, for Alert and only, as it doesn't implement the 'hide' method
      instance[method]();
    });
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap alert.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$f = 'alert';
  const DATA_KEY$a = 'bs.alert';
  const EVENT_KEY$b = `.${DATA_KEY$a}`;
  const EVENT_CLOSE = `close${EVENT_KEY$b}`;
  const EVENT_CLOSED = `closed${EVENT_KEY$b}`;
  const CLASS_NAME_FADE$5 = 'fade';
  const CLASS_NAME_SHOW$8 = 'show';

  /**
   * Class definition
   */

  class Alert extends BaseComponent {
    // Getters
/**
* @description This function is a static method that returns the value of a constant
* named `NAME`. The `$f` at the end of the return statement indicates that the
* returned value is a frozen string literals.
* 
* @returns { string } The output returned by this function is "undefined".
* 
* The reason is that the variable `NAME` has not been defined yet.
*/
    static get NAME() {
      return NAME$f;
    }

    // Public
/**
* @description This function close() triggers an event and removes a class name from
* the element then calls a queueCallback after delay if the element has animation
* and eventually destroys the element
* 
* @returns {  } This function returns undefined.
*/
    close() {
      const closeEvent = EventHandler.trigger(this._element, EVENT_CLOSE);
      if (closeEvent.defaultPrevented) {
        return;
      }
      this._element.classList.remove(CLASS_NAME_SHOW$8);
      const isAnimated = this._element.classList.contains(CLASS_NAME_FADE$5);
      this._queueCallback(() => this._destroyElement(), this._element, isAnimated);
    }

    // Private
/**
* @description This function destroys the element associated with the widget and
* releases resources by removing the element and triggering an event to indicate closure.
* 
* @returns { any } Based on the code snippet provided:
* 
* The `destroyElement()` function removes the `_element` from the DOM using `remove()`
* method and triggers an `EVENT_CLOSED` event on it.
*/
    _destroyElement() {
      this._element.remove();
      EventHandler.trigger(this._element, EVENT_CLOSED);
      this.dispose();
    }

    // Static
/**
* @description This function is a static method on the jQuery object that allows you
* to call methods on all matched elements using string method names. It takes an
* optional `config` argument that specifies the method name to call. If the method
* does not exist or starts with an underscore ('_'), it throws a TypeError.
* 
* @param { object } config - In the provided jQuery Interface function (i.e., `static
* jQueryInterface(config)`), the `config` input parameter is used to pass a method
* name or multiple method names to be called on the current instance of Alert. If
* `config` is a string and not undefined or empty String(''), then the function calls
* that specified method on each element (i.e., DOM element) currently being traversed
* using `this`.
* 
* @returns { object } The function `jQueryInterface` returns `this`, which means
* that the function does not return any value explicitly but instead returns the
* current object (probably an element) that was passed as the first argument to the
* `each` method.
*/
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Alert.getOrCreateInstance(this);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config](this);
      });
    }
  }

  /**
   * Data API implementation
   */

  enableDismissTrigger(Alert, 'close');

  /**
   * jQuery
   */

  defineJQueryPlugin(Alert);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap button.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$e = 'button';
  const DATA_KEY$9 = 'bs.button';
  const EVENT_KEY$a = `.${DATA_KEY$9}`;
  const DATA_API_KEY$6 = '.data-api';
  const CLASS_NAME_ACTIVE$3 = 'active';
  const SELECTOR_DATA_TOGGLE$5 = '[data-bs-toggle="button"]';
  const EVENT_CLICK_DATA_API$6 = `click${EVENT_KEY$a}${DATA_API_KEY$6}`;

  /**
   * Class definition
   */

  class Button extends BaseComponent {
    // Getters
/**
* @description This function is agetter method that returns the value of the property
* 'NAME$e' ( Note the dollar sign at the end of the property name).
* 
* @returns { string } The function returns `NAME$e`, which is an undefined value
* since `NAME` is not defined.
*/
    static get NAME() {
      return NAME$e;
    }

    // Public
/**
* @description This function toggle() on an element is used to add and remove a class
* name (CLASS_NAME_ACTIVE) based on the return value of the .toggle() method.
* 
* @returns { boolean } The output returned by this function is a boolean value
* indicating whether the toggle() method returned true or false.
*/
    toggle() {
      // Toggle class and sync the `aria-pressed` attribute with the return value of the `.toggle()` method
      this._element.setAttribute('aria-pressed', this._element.classList.toggle(CLASS_NAME_ACTIVE$3));
    }

    // Static
/**
* @description This function is a jQuery plugin that provides a `toggle` method for
* buttons.
* 
* @param { string } config - Based on the function's implementation:
* 
* In `static jQueryInterface(config)`, `config` determines the button state to apply
* when called on an element.
* 
* @returns {  } This function takes a `config` parameter and returns the result of
* applying the configured action to each button element within the set of elements
* selected by the `this` keyword.
* 
* The function returns `this`, allowing the caller to chain additional method calls
* onto the returned instance.
* 
* In plain English: the function takes an object with a configuration property
* (`config`), and applies that configuration to each button element it finds inside
* the set of elements selected by `this`.
*/
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Button.getOrCreateInstance(this);
        if (config === 'toggle') {
          data[config]();
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$6, SELECTOR_DATA_TOGGLE$5, event => {
    event.preventDefault();
    const button = event.target.closest(SELECTOR_DATA_TOGGLE$5);
    const data = Button.getOrCreateInstance(button);
    data.toggle();
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Button);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/swipe.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$d = 'swipe';
  const EVENT_KEY$9 = '.bs.swipe';
  const EVENT_TOUCHSTART = `touchstart${EVENT_KEY$9}`;
  const EVENT_TOUCHMOVE = `touchmove${EVENT_KEY$9}`;
  const EVENT_TOUCHEND = `touchend${EVENT_KEY$9}`;
  const EVENT_POINTERDOWN = `pointerdown${EVENT_KEY$9}`;
  const EVENT_POINTERUP = `pointerup${EVENT_KEY$9}`;
  const POINTER_TYPE_TOUCH = 'touch';
  const POINTER_TYPE_PEN = 'pen';
  const CLASS_NAME_POINTER_EVENT = 'pointer-event';
  const SWIPE_THRESHOLD = 40;
  const Default$c = {
    endCallback: null,
    leftCallback: null,
    rightCallback: null
  };
  const DefaultType$c = {
    endCallback: '(function|null)',
    leftCallback: '(function|null)',
    rightCallback: '(function|null)'
  };

  /**
   * Class definition
   */

  class Swipe extends Config {
/**
* @description This constructor function initializes a new Swipe object and sets up
* event listeners to handle swipe gestures on an element.
* 
* @param {  } element - The `element` parameter is the DOM element on which the Swipe
* gesture recognition will be applied.
* 
* @param { object } config - The `config` input parameter is used to pass configuration
* options for the Swipe object to the constructor.
* 
* @returns {  } The function takes an `element` and a `config` object as inputs and
* returns nothing (since it doesn't have a `return` statement).
*/
    constructor(element, config) {
      super();
      this._element = element;
      if (!element || !Swipe.isSupported()) {
        return;
      }
      this._config = this._getConfig(config);
      this._deltaX = 0;
      this._supportPointerEvents = Boolean(window.PointerEvent);
      this._initEvents();
    }

    // Getters
/**
* @description This function is a static method that returns the `Default` instance
* of an object.
* 
* @returns { string } The output returned by this function is `undefined`.
* 
* The reason for this is that the `Default` function is static and does not have an
* explicit return statement. According to JavaScript syntax rules. the absence of a
* return statement implies that `undefined` is returned.
*/
    static get Default() {
      return Default$c;
    }
/**
* @description This function is a `getter` method that returns the value of the
* static variable `DefaultType$c`.
* 
* @returns { string } The output returned by this function is `DefaultType$c`.
*/
    static get DefaultType() {
      return DefaultType$c;
    }
/**
* @description The function returns the value of the `NAME$d` static field.
* 
* @returns { string } The output returned by this function is `NAME$d`.
*/
    static get NAME() {
      return NAME$d;
    }

    // Public
/**
* @description The provided function `dispose()` disposingly detaches an event handler
* from the `EVENT_KEY$9` event on the element it is attached to.
* 
* @returns {  } The function `dispose` has no return statement and returns undefined
* by default.
*/
    dispose() {
      EventHandler.off(this._element, EVENT_KEY$9);
    }

    // Private
/**
* @description This function (`_start`) handles touch events for the widget.
* 
* @param {  } event - The `event` input parameter receives an event object that
* contains information about the user interaction (such as mouse or touch movement).
* In this function specifically `event.touches[0].clientX;` accesses the client-side
* coordinates of the event touchpoint.
* 
* @returns {  } The function takes an `event` object as input and returns nothing
* (since it's undefined). It checks if the event is a touch event and if it is a pen
* touch event. If it's a pen touch event (`_eventIsPointerPenTouch(event)` is true),
* it sets the `_deltaX` property to `event.clientX`. Otherwise (`this._supportPointerEvents`
* is falsey), it sets `_deltaX` to `event.touches[0].clientX`. In other words:
* 
* 	- If `event.type` is not a touch event or if `event.touches` is empty
* (`event.touches.length = 0`), the function does nothing and returns no output
* (since `undefined`).
* 	- If `event.touches.length > 0`, it tries to get the client X of the first touch
* point using `event.touches[0].clientX`.
*/
    _start(event) {
      if (!this._supportPointerEvents) {
        this._deltaX = event.touches[0].clientX;
        return;
      }
      if (this._eventIsPointerPenTouch(event)) {
        this._deltaX = event.clientX;
      }
    }
/**
* @description This function is an event handler that listens for the `_end` event
* and performs the following actions:
* 
* 1/ Checks if the event is a pointer pen touch event.
* 2/ Calculates the delta x-coordinate of the touch movement since the last event.
* 3/ Calls the `_handleSwipe` method.
* 4/ Executes the configured `endCallback`.
* 
* @param { object } event - The `event` input parameter is an object containing
* information about the user's gesture or interaction with the page.
* 
* @returns {  } The function takes an `event` parameter and returns nothing (i.e.,
* it is a void function). The output of the function is not defined. The function
* performs some logic related to touch events and calls other functions like
* `_handleSwipe()` and `execute()`, but the output of these functions is not specified.
*/
    _end(event) {
      if (this._eventIsPointerPenTouch(event)) {
        this._deltaX = event.clientX - this._deltaX;
      }
      this._handleSwipe();
      execute(this._config.endCallback);
    }
/**
* @description This function implements the functionality to move an object when the
* user scrolls or drags it using touch gestures.
* 
* @param {  } event - The `event` input parameter is passed as an argument to the
* function and provides information about the current touch event that triggered the
* function call.
* 
* @returns {  } The output returned by this function is `0`.
* 
* Here's a concise description of what the function does:
* 
* If the event object contains multiple touches (i.e., `event.touches &&
* event.touches.length > 1`), then the function returns `0`.
*/
    _move(event) {
      this._deltaX = event.touches && event.touches.length > 1 ? 0 : event.touches[0].clientX - this._deltaX;
    }
/**
* @description This function implements a swipe gesture recognition on a React
* component. It determines the direction of the swipe (left or right) based on the
* distance and angle of the finger's movement on the screen.
* 
* @returns {  } The output returned by `_handleSwipe()` is void. The function does
* not return any value explicitly.
*/
    _handleSwipe() {
      const absDeltaX = Math.abs(this._deltaX);
      if (absDeltaX <= SWIPE_THRESHOLD) {
        return;
      }
      const direction = absDeltaX / this._deltaX;
      this._deltaX = 0;
      if (!direction) {
        return;
      }
      execute(direction > 0 ? this._config.rightCallback : this._config.leftCallback);
    }
/**
* @description This function sets up event listeners for the `_element` element to
* handle pointer or touch events (depending on the browser support), including
* `EVENT_POINTERDOWN`, `EVENT_POINTERUP`, `EVENT_TOUCHSTART`, `EVENT_TOUCHMOVE`, and
* `EVENT_TOUCHEND`.
* 
* @returns {  } This function adds event listeners to an element for pointer events
* or touch events depending on support for pointer events.
*/
    _initEvents() {
      if (this._supportPointerEvents) {
        EventHandler.on(this._element, EVENT_POINTERDOWN, event => this._start(event));
        EventHandler.on(this._element, EVENT_POINTERUP, event => this._end(event));
        this._element.classList.add(CLASS_NAME_POINTER_EVENT);
      } else {
        EventHandler.on(this._element, EVENT_TOUCHSTART, event => this._start(event));
        EventHandler.on(this._element, EVENT_TOUCHMOVE, event => this._move(event));
        EventHandler.on(this._element, EVENT_TOUCHEND, event => this._end(event));
      }
    }
/**
* @description This function checks if the event object passed to it represents a
* pen touch or not by checking the `pointerType` property of the event object and
* returning `true` if it is either `POINTER_TYPE_PEN` or `POINTER_TYPE_TOUCH`.
* 
* @param { object } event - The `event` input parameter is passed as an argument to
* the function and is used to determine whether the current event is a pen or touch
* event.
* 
* @returns { boolean } Based on the code snippet provided:
* 
* The output returned by the function `_eventIsPointerPenTouch(event)` is a boolean
* value that indicates whether the given `event` object is a pen touch event or not.
*/
    _eventIsPointerPenTouch(event) {
      return this._supportPointerEvents && (event.pointerType === POINTER_TYPE_PEN || event.pointerType === POINTER_TYPE_TOUCH);
    }

    // Static
/**
* @description This function checks if the device supports touch events by checking
* the `ontouchstart` property of the document element and the `navigator.maxTouchPoints`
* property.
* 
* @returns { boolean } The output returned by this function is a Boolean value
* indicating whether the browser supports touch events. The function checks if the
* `ontouchstart` property exists on the document element or if the `navigator.maxTouchPoints`
* property is greater than 0. If either of these conditions is true (i.e., the browser
* supports touch events), then the function returns `true`.
*/
    static isSupported() {
      return 'ontouchstart' in document.documentElement || navigator.maxTouchPoints > 0;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap carousel.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$c = 'carousel';
  const DATA_KEY$8 = 'bs.carousel';
  const EVENT_KEY$8 = `.${DATA_KEY$8}`;
  const DATA_API_KEY$5 = '.data-api';
  const ARROW_LEFT_KEY$1 = 'ArrowLeft';
  const ARROW_RIGHT_KEY$1 = 'ArrowRight';
  const TOUCHEVENT_COMPAT_WAIT = 500; // Time for mouse compat events to fire after touch

  const ORDER_NEXT = 'next';
  const ORDER_PREV = 'prev';
  const DIRECTION_LEFT = 'left';
  const DIRECTION_RIGHT = 'right';
  const EVENT_SLIDE = `slide${EVENT_KEY$8}`;
  const EVENT_SLID = `slid${EVENT_KEY$8}`;
  const EVENT_KEYDOWN$1 = `keydown${EVENT_KEY$8}`;
  const EVENT_MOUSEENTER$1 = `mouseenter${EVENT_KEY$8}`;
  const EVENT_MOUSELEAVE$1 = `mouseleave${EVENT_KEY$8}`;
  const EVENT_DRAG_START = `dragstart${EVENT_KEY$8}`;
  const EVENT_LOAD_DATA_API$3 = `load${EVENT_KEY$8}${DATA_API_KEY$5}`;
  const EVENT_CLICK_DATA_API$5 = `click${EVENT_KEY$8}${DATA_API_KEY$5}`;
  const CLASS_NAME_CAROUSEL = 'carousel';
  const CLASS_NAME_ACTIVE$2 = 'active';
  const CLASS_NAME_SLIDE = 'slide';
  const CLASS_NAME_END = 'carousel-item-end';
  const CLASS_NAME_START = 'carousel-item-start';
  const CLASS_NAME_NEXT = 'carousel-item-next';
  const CLASS_NAME_PREV = 'carousel-item-prev';
  const SELECTOR_ACTIVE = '.active';
  const SELECTOR_ITEM = '.carousel-item';
  const SELECTOR_ACTIVE_ITEM = SELECTOR_ACTIVE + SELECTOR_ITEM;
  const SELECTOR_ITEM_IMG = '.carousel-item img';
  const SELECTOR_INDICATORS = '.carousel-indicators';
  const SELECTOR_DATA_SLIDE = '[data-bs-slide], [data-bs-slide-to]';
  const SELECTOR_DATA_RIDE = '[data-bs-ride="carousel"]';
  const KEY_TO_DIRECTION = {
    [ARROW_LEFT_KEY$1]: DIRECTION_RIGHT,
    [ARROW_RIGHT_KEY$1]: DIRECTION_LEFT
  };
  const Default$b = {
    interval: 5000,
    keyboard: true,
    pause: 'hover',
    ride: false,
    touch: true,
    wrap: true
  };
  const DefaultType$b = {
    interval: '(number|boolean)',
    // TODO:v6 remove boolean support
    keyboard: 'boolean',
    pause: '(string|boolean)',
    ride: '(boolean|string)',
    touch: 'boolean',
    wrap: 'boolean'
  };

  /**
   * Class definition
   */

  class Carousel extends BaseComponent {
/**
* @description This function is the constructor for a carousel component. It sets
* up the internal state of the component (such as the current element being slided
* and the interval timer) and adds event listeners to the carousel. Additionally it
* initializes a swipe helper and an indicators element if configured.
* 
* @param { object } element - The `element` parameter is the container element where
* the carousel will be appended and represents the HTML element that the carousel
* will be attached to.
* 
* @param { object } config - The `config` input parameter is an object that contains
* configuration properties for the Carousel constructor.
* 
* @returns {  } This function constructs a new instance of the Carousel class and
* sets its properties and event listeners.
*/
    constructor(element, config) {
      super(element, config);
      this._interval = null;
      this._activeElement = null;
      this._isSliding = false;
      this.touchTimeout = null;
      this._swipeHelper = null;
      this._indicatorsElement = SelectorEngine.findOne(SELECTOR_INDICATORS, this._element);
      this._addEventListeners();
      if (this._config.ride === CLASS_NAME_CAROUSEL) {
        this.cycle();
      }
    }

    // Getters
/**
* @description This function is a getter method that returns the value of the `Default`
* static field of the current class.
* 
* @returns { string } The output returned by the function is `Default$b`.
*/
    static get Default() {
      return Default$b;
    }
/**
* @description This function is a getter method for the `DefaultType` property of
* the class and returns a constant value named `DefaultType$b`.
* 
* @returns { string } The function `get DefaultType()` returns the value `$b`.
*/
    static get DefaultType() {
      return DefaultType$b;
    }
/**
* @description This function is a getter method that returns the value of the "NAME"
* constant as a string.
* 
* @returns { string } The function `getName` returns undefined because the variable
* `NAME$c` is never defined or initialized.
*/
    static get NAME() {
      return NAME$c;
    }

    // Public
/**
* @description This function calls the `_slide()` method with the `ORDER_NEXT`
* parameter to move to the next slide.
* 
* @returns { object } This function does not return any value as it is an empty
* function with no statements inside.
*/
    next() {
      this._slide(ORDER_NEXT);
    }
/**
* @description This function calls the `next()` method on the current carousel
* instance when the page is visible and the carousel and its parent element are also
* visible.
* 
* @returns { any } The `nextWhenVisible()` function takes no arguments and has a
* single line of code that checks if the page and the carousel's parent element are
* visible and then calls the `next()` function if they are.
* 
* Therefore the output of this function is to call the `next()` function of the
* parent object if the page and the carousel's parent element are visible.
*/
    nextWhenVisible() {
      // FIXME TODO use `document.visibilityState`
      // Don't call next when the page isn't visible
      // or the carousel or its parent isn't visible
      if (!document.hidden && isVisible(this._element)) {
        this.next();
      }
    }
/**
* @description This function causes the current slide to move to the previous slide.
* 
* @returns { any } The function `prev()` returns `this`. It does not return any value
* explicitly but instead returns the current instance of the object itself.
*/
    prev() {
      this._slide(ORDER_PREV);
    }
/**
* @description The `pause()` function pauses the slide animation by:
* 
* 1/ Checking if the slider is currently sliding ( `_isSliding` is truthy).
* 2/ Triggering the "transitionend" event on the element to pause the transition.
* 3/ Clearing any existing timer intervals.
* 
* @returns { any } The function `pause` takes no arguments and has a return type of
* `undefined`. It clears any scheduled transitions and checks if there is currently
* a sliding animation active on the element associated with the instance of the
* class. If an animation is active it calls the `transitionEnd` event triggerer and
* then cleares an interval that may have been set for later animation processing.
*/
    pause() {
      if (this._isSliding) {
        triggerTransitionEnd(this._element);
      }
      this._clearInterval();
    }
/**
* @description This function starts or resumes the animation of an object using a
* interval loop.
* 
* @returns {  } The output of the `cycle` function is undefined. This is because the
* function does not return anything (it does not have a `return` statement).
*/
    cycle() {
      this._clearInterval();
      this._updateInterval();
      this._interval = setInterval(() => this.nextWhenVisible(), this._config.interval);
    }
/**
* @description This function prepares the Carousel component to start a new cycle
* of slides by:
* 
* 1/ Checking if the component is enabled and if there are any slides to show.
* 2/ Adding an event listener to the slider element to trigger the cycle function
* when the user slides the carousel.
* 3/ Calling the cycle function immediately if the component is not currently sliding.
* 
* @returns { any } The `maybeEnableCycle` function returns nothing (void) or does
* not return anything explicit (i.e., `undefined`). It only executes code and handles
* events if certain conditions are met.
*/
    _maybeEnableCycle() {
      if (!this._config.ride) {
        return;
      }
      if (this._isSliding) {
        EventHandler.one(this._element, EVENT_SLID, () => this.cycle());
        return;
      }
      this.cycle();
    }
/**
* @description This function moves the currently displayed slide to a specific index
* within the list of slides.
* 
* @param { number } index - The `index` input parameter specifies the position of
* the item to slide to. It should be a positive integer less than or equal to the
* length of the `items` array.
* 
* @returns {  } The output of the function is:
* 
* 	- void (no value is returned)
* 
* The function does not return anything.
*/
    to(index) {
      const items = this._getItems();
      if (index > items.length - 1 || index < 0) {
        return;
      }
      if (this._isSliding) {
        EventHandler.one(this._element, EVENT_SLID, () => this.to(index));
        return;
      }
      const activeIndex = this._getItemIndex(this._getActive());
      if (activeIndex === index) {
        return;
      }
      const order = index > activeIndex ? ORDER_NEXT : ORDER_PREV;
      this._slide(order, items[index]);
    }
/**
* @description This function is the `dispose()` method of an object.
* 
* @returns {  } The output of the `dispose()` function is not explicitly specified
* but can be inferred from the code. The function first calls `super.dispose()`,
* which means that it invokes the inherited implementation of `dispose()`. This
* likely results for cleaning up resources held by the parent object.
* 
* Additionally), the function also disposes the `_swipeHelper` object.
*/
    dispose() {
      if (this._swipeHelper) {
        this._swipeHelper.dispose();
      }
      super.dispose();
    }

    // Private
/**
* @description The function `configAfterMerge` updates the `defaultInterval` property
* of the input `config` object to match the value of the `interval` property.
* 
* @param { object } config - In the given function `_configAfterMerge`, the `config`
* input parameter is an object that contains the final configuration values after
* merging any override configs. The function simply modifies a single property of
* this object (`defaultInterval`) and returns the modified config object unchanged.
* 
* @returns { object } The function `_configAfterMerge(config)` takes a `config`
* object as an argument and modifies it by setting its `defaultInterval` property
* to the value of its `interval` property.
*/
    _configAfterMerge(config) {
      config.defaultInterval = config.interval;
      return config;
    }
/**
* @description This function adds event listeners to the specified element for various
* events related to keyboard and mouse inputs as well as touch inputs if supported.
* 
* @returns { any } This function adds event listeners to an element based on certain
* conditions. The output is a list of event listeners that have been added to the element.
*/
    _addEventListeners() {
      if (this._config.keyboard) {
        EventHandler.on(this._element, EVENT_KEYDOWN$1, event => this._keydown(event));
      }
      if (this._config.pause === 'hover') {
        EventHandler.on(this._element, EVENT_MOUSEENTER$1, () => this.pause());
        EventHandler.on(this._element, EVENT_MOUSELEAVE$1, () => this._maybeEnableCycle());
      }
      if (this._config.touch && Swipe.isSupported()) {
        this._addTouchEventListeners();
      }
    }
/**
* @description This function adds event listeners for touch events (touchstart/touchend)
* to the image elements within the carousel and sets up a swipe gesture recognizer
* to simulate mouseover and drag-style navigation.
* 
* @returns { object } The function `_addTouchEventListeners()` returns nothing (i.e.,
* it has no output).
*/
    _addTouchEventListeners() {
      for (const img of SelectorEngine.find(SELECTOR_ITEM_IMG, this._element)) {
        EventHandler.on(img, EVENT_DRAG_START, event => event.preventDefault());
      }
/**
* @description This function implements touch-related logic for a carousel.
* 
* @returns {  } The output returned by this function is `undefined`.
*/
      const endCallBack = () => {
        if (this._config.pause !== 'hover') {
          return;
        }

        // If it's a touch-enabled device, mouseenter/leave are fired as
        // part of the mouse compatibility events on first tap - the carousel
        // would stop cycling until user tapped out of it;
        // here, we listen for touchend, explicitly pause the carousel
        // (as if it's the second time we tap on it, mouseenter compat event
        // is NOT fired) and after a timeout (to allow for mouse compatibility
        // events to fire) we explicitly restart cycling

        this.pause();
        if (this.touchTimeout) {
          clearTimeout(this.touchTimeout);
        }
        this.touchTimeout = setTimeout(() => this._maybeEnableCycle(), TOUCHEVENT_COMPAT_WAIT + this._config.interval);
      };
      const swipeConfig = {
/**
* @description The function `leftCallback` is a callback function that will be called
* when the user slides the element left.
* 
* @returns { object } The function `leftCallback` is a callback function that takes
* no arguments and returns `this._slide(this._directionToOrder(DIRECTION_LEFT))`
* which is essentially the same as `this._slide(LEFT)`.
* 
* In other words., the output of this function is the value of `this._slide(LEFT)`,
* which is not specified.
*/
        leftCallback: () => this._slide(this._directionToOrder(DIRECTION_LEFT)),
/**
* @description This function registers a callback function that will be called when
* the user scrolls to the right.
* 
* @returns { any } The output returned by the `rightCallback` function is
* `this._slide(this._directionToOrder(DIRECTION_RIGHT))` which is a call to the
* `_slide` method with the `DIRECTION_RIGHT` value as its argument.
*/
        rightCallback: () => this._slide(this._directionToOrder(DIRECTION_RIGHT)),
        endCallback: endCallBack
      };
      this._swipeHelper = new Swipe(this._element, swipeConfig);
    }
/**
* @description This function is a keyboard handler that listens for key presses on
* an HTML element and responds by sliding the element to a specific position based
* on the key pressed.
* 
* @param { object } event - In the given code snippet `${event}` is an event object
* passed as an argument to `_keydown()` function whenever any key is pressed on the
* page and triggered by that function call.
* 
* @returns {  } The function `_keydown` takes an `event` object as an argument and
* returns nothing (it is an undefined function). It checks if the target element of
* the event is an input or textarea element using a regular expression test. If it
* is not one of those elements. It then checks for the keyboard direction using an
* array of keycodes mapped to directions. If there is a matching direction keycode.
*/
    _keydown(event) {
      if (/input|textarea/i.test(event.target.tagName)) {
        return;
      }
      const direction = KEY_TO_DIRECTION[event.key];
      if (direction) {
        event.preventDefault();
        this._slide(this._directionToOrder(direction));
      }
    }
/**
* @description This function returns the index of an element within an array of items
* (represented by `this._getItems()`) within the calling object.
* 
* @param {  } element - The `element` input parameter is the object being searched
* for within the `this._getItems()` array.
* 
* @returns { integer } The function `_getItemIndex(element)` returns the index of
* the element within the list of items stored on this object.
*/
    _getItemIndex(element) {
      return this._getItems().indexOf(element);
    }
/**
* @description This function sets the active indicator element to the specified index
* among the slide indicators.
* 
* @param { number } index - The `index` input parameter specifies which indicator
* element should be activated (or highlighted) next.
* 
* @returns {  } This function takes an index as input and sets the active indicator
* element based on that index.
*/
    _setActiveIndicatorElement(index) {
      if (!this._indicatorsElement) {
        return;
      }
      const activeIndicator = SelectorEngine.findOne(SELECTOR_ACTIVE, this._indicatorsElement);
      activeIndicator.classList.remove(CLASS_NAME_ACTIVE$2);
      activeIndicator.removeAttribute('aria-current');
      const newActiveIndicator = SelectorEngine.findOne(`[data-bs-slide-to="${index}"]`, this._indicatorsElement);
      if (newActiveIndicator) {
        newActiveIndicator.classList.add(CLASS_NAME_ACTIVE$2);
        newActiveIndicator.setAttribute('aria-current', 'true');
      }
    }
/**
* @description This function updates the interval value based on the `data-bs-interval`
* attribute of the active element and stores it as the new interval for the carousel
* configuration.
* 
* @returns {  } This function takes an HTML element and returns the value of its
* "data-bs-interval" attribute or the default interval if no such attribute exists.
*/
    _updateInterval() {
      const element = this._activeElement || this._getActive();
      if (!element) {
        return;
      }
      const elementInterval = Number.parseInt(element.getAttribute('data-bs-interval'), 10);
      this._config.interval = elementInterval || this._config.defaultInterval;
    }
/**
* @description This function allows an element to slide to a specified next element
* based on a defined order and animation settings.
* 
* @param {  } order - The `order` input parameter determines the direction of the slide:
* 
* 	- `ORDER_NEXT`: moves the active element to the next slide
* 	- `ORDER_PREV`: moves the active element to the previous slide
* 
* @param {  } element - The `element` input parameter allows the function to select
* a specific element within the carousel that should be the next one to become active.
* 
* @returns {  } The `slide` function takes two parameters: `order` and `element`.
* It returns nothing; instead it performs various actions and updates the carousel's
* state.
*/
    _slide(order, element = null) {
      if (this._isSliding) {
        return;
      }
      const activeElement = this._getActive();
      const isNext = order === ORDER_NEXT;
      const nextElement = element || getNextActiveElement(this._getItems(), activeElement, isNext, this._config.wrap);
      if (nextElement === activeElement) {
        return;
      }
      const nextElementIndex = this._getItemIndex(nextElement);
/**
* @description This function triggers an event (of the specified `eventName`) on the
* provided `nextElement`, passing along information about the current active element
* and the direction of the trigger (based on the `_orderToDirection` function).
* 
* @param { string } eventName - The `eventName` parameter passed to `triggerEvent`
* represents the name of the event that should be triggered. This is typically a
* string representing the type of event (e.g.
* 
* @returns { object } This function takes an `eventName` parameter and returns an
* object that represents an event trigger with information such as `relatedTarget`,
* `direction`, `from`, and `to`.
*/
      const triggerEvent = eventName => {
        return EventHandler.trigger(this._element, eventName, {
          relatedTarget: nextElement,
          direction: this._orderToDirection(order),
          from: this._getItemIndex(activeElement),
          to: nextElementIndex
        });
      };
      const slideEvent = triggerEvent(EVENT_SLIDE);
      if (slideEvent.defaultPrevented) {
        return;
      }
      if (!activeElement || !nextElement) {
        // Some weirdness is happening, so we bail
        // TODO: change tests that use empty divs to avoid this check
        return;
      }
      const isCycling = Boolean(this._interval);
      this.pause();
      this._isSliding = true;
      this._setActiveIndicatorElement(nextElementIndex);
      this._activeElement = nextElement;
      const directionalClassName = isNext ? CLASS_NAME_START : CLASS_NAME_END;
      const orderClassName = isNext ? CLASS_NAME_NEXT : CLASS_NAME_PREV;
      nextElement.classList.add(orderClassName);
      reflow(nextElement);
      activeElement.classList.add(directionalClassName);
      nextElement.classList.add(directionalClassName);
/**
* @description This function sets up the callback for the transition end event of a
* slide item and performs the following actions:
* 
* 1/ Removes the directional and order class names from the previous element.
* 2/ Adds the CLASS_NAME_ACTIVE$2 name to the next element.
* 3/ Removes the CLASS_NAME_ACTIVE$2 and directional class names from the active element.
* 4/ Sets the _isSliding property to false.
* 5/ Triggers the EVENT_SLID event.
* 
* @returns {  } The output of the given function is an object with several methods
* and properties for handling slide transitions.
*/
      const completeCallBack = () => {
        nextElement.classList.remove(directionalClassName, orderClassName);
        nextElement.classList.add(CLASS_NAME_ACTIVE$2);
        activeElement.classList.remove(CLASS_NAME_ACTIVE$2, orderClassName, directionalClassName);
        this._isSliding = false;
        triggerEvent(EVENT_SLID);
      };
      this._queueCallback(completeCallBack, activeElement, this._isAnimated());
      if (isCycling) {
        this.cycle();
      }
    }
/**
* @description This function checks if the element has the `CLASS_NAME_SLIDE` class
* active on it. If it does have that class present and applied then this method will
* return `true`.
* 
* @returns { boolean } The output returned by this function is a Boolean value (true
* or false) indicating whether the element has the class name "slide" or not.
*/
    _isAnimated() {
      return this._element.classList.contains(CLASS_NAME_SLIDE);
    }
/**
* @description This function returns the currently active item from a list of items
* using the `SelectorEngine` to find the matching element.
* 
* @returns {  } This function is calling `SelectorEngine.findOne()` with
* `SELECTOR_ACTIVE_ITEM` and passing `this._element` as an argument. Since `this._element`
* is undefined at this point of time when the function is being executed. SelectorEngine
* won't find anything and return undefined or empty collection accordingly.
*/
    _getActive() {
      return SelectorEngine.findOne(SELECTOR_ACTIVE_ITEM, this._element);
    }
/**
* @description This function `_getItems()` returns all elements that match the
* selector string `SELECTOR_ITEM` within the element passed as an argument to the
* function (`this._element`).
* 
* @returns { array } The output of the `getItems()` function is an array of elements
* selected using the `Selector Engine` and specified by the `SELECTOR_ITEM` variable.
*/
    _getItems() {
      return SelectorEngine.find(SELECTOR_ITEM, this._element);
    }
/**
* @description This function is a method of an object and it clears any interval
* that may have been set previously by using the `clearInterval()` method and sets
* the interval variable to null.
* 
* @returns { any } This function clears any previously set interval and sets the
* interval variable to null.
* 
* Output: void (nothing is returned).
*/
    _clearInterval() {
      if (this._interval) {
        clearInterval(this._interval);
        this._interval = null;
      }
    }
/**
* @description This function determines the order to be used when rendering elements
* based on a given direction ( LEFT or RIGHT ) and the directionality of the layout
* (RTL or LTR).
* 
* @param { string } direction - The `direction` parameter specifies the navigation
* direction (left or right) that should be ordered next/previous.
* 
* @returns {  } The function takes a `direction` parameter and returns one of two
* possible values based on whether the direction is "left" or "right" and whether
* the language is RTL (Right-to-Left) or LTR (Left-to-Right).
* 
* In LTR languages:
* 
* 	- If `direction` is "left", the function returns `ORDER_NEXT`.
* 	- If `direction` is "right", the function returns `ORDER_PREV`.
* 
* In RTL languages:
* 
* 	- If `direction` is "left", the function returns `ORDER_PREV`.
* 	- If `direction` is "right`, the function returns `ORDER_NEXT`.
* 
* So the output returned by this function depends on the value of `direction` and
* the directionality of the language.
*/
    _directionToOrder(direction) {
      if (isRTL()) {
        return direction === DIRECTION_LEFT ? ORDER_PREV : ORDER_NEXT;
      }
      return direction === DIRECTION_LEFT ? ORDER_NEXT : ORDER_PREV;
    }
/**
* @description This function takes an order value as input and returns a direction
* value based on the order and the text direction of the page.
* 
* @param { string } order - The `order` parameter passed into `_orderToDirection()`
* is a value indicating the direction of the order (either `ORDER_PREV` or `ORDER_NEXT`),
* and it determines which direction the function returns.
* 
* @returns { string } This function takes an `order` parameter and returns a direction
* based on the order and the reading direction of the language.
* 
* For languages that read from right to left (RTL), the function returns the opposite
* direction as the order.
*/
    _orderToDirection(order) {
      if (isRTL()) {
        return order === ORDER_PREV ? DIRECTION_LEFT : DIRECTION_RIGHT;
      }
      return order === ORDER_PREV ? DIRECTION_RIGHT : DIRECTION_LEFT;
    }

    // Static
/**
* @description This function is the jQuery interface for the Carousel widget. It
* takes a configuration object and applies it to theCarousel instance associated
* with the current element.
* 
* @param { object } config - The `config` input parameter is an object or a number
* that defines the configuration for the carousel.
* 
* @returns {  } The function `jQueryInterface` returns `this` (the current element
* being processed) after iterating through each element and performing the specified
* actions on the `data` object associated with that element using the provided `config`.
*/
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Carousel.getOrCreateInstance(this, config);
        if (typeof config === 'number') {
          data.to(config);
          return;
        }
        if (typeof config === 'string') {
          if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
            throw new TypeError(`No method named "${config}"`);
          }
          data[config]();
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$5, SELECTOR_DATA_SLIDE, function (event) {
    const target = SelectorEngine.getElementFromSelector(this);
    if (!target || !target.classList.contains(CLASS_NAME_CAROUSEL)) {
      return;
    }
    event.preventDefault();
    const carousel = Carousel.getOrCreateInstance(target);
    const slideIndex = this.getAttribute('data-bs-slide-to');
    if (slideIndex) {
      carousel.to(slideIndex);
      carousel._maybeEnableCycle();
      return;
    }
    if (Manipulator.getDataAttribute(this, 'slide') === 'next') {
      carousel.next();
      carousel._maybeEnableCycle();
      return;
    }
    carousel.prev();
    carousel._maybeEnableCycle();
  });
  EventHandler.on(window, EVENT_LOAD_DATA_API$3, () => {
    const carousels = SelectorEngine.find(SELECTOR_DATA_RIDE);
    for (const carousel of carousels) {
      Carousel.getOrCreateInstance(carousel);
    }
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Carousel);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap collapse.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$b = 'collapse';
  const DATA_KEY$7 = 'bs.collapse';
  const EVENT_KEY$7 = `.${DATA_KEY$7}`;
  const DATA_API_KEY$4 = '.data-api';
  const EVENT_SHOW$6 = `show${EVENT_KEY$7}`;
  const EVENT_SHOWN$6 = `shown${EVENT_KEY$7}`;
  const EVENT_HIDE$6 = `hide${EVENT_KEY$7}`;
  const EVENT_HIDDEN$6 = `hidden${EVENT_KEY$7}`;
  const EVENT_CLICK_DATA_API$4 = `click${EVENT_KEY$7}${DATA_API_KEY$4}`;
  const CLASS_NAME_SHOW$7 = 'show';
  const CLASS_NAME_COLLAPSE = 'collapse';
  const CLASS_NAME_COLLAPSING = 'collapsing';
  const CLASS_NAME_COLLAPSED = 'collapsed';
  const CLASS_NAME_DEEPER_CHILDREN = `:scope .${CLASS_NAME_COLLAPSE} .${CLASS_NAME_COLLAPSE}`;
  const CLASS_NAME_HORIZONTAL = 'collapse-horizontal';
  const WIDTH = 'width';
  const HEIGHT = 'height';
  const SELECTOR_ACTIVES = '.collapse.show, .collapse.collapsing';
  const SELECTOR_DATA_TOGGLE$4 = '[data-bs-toggle="collapse"]';
  const Default$a = {
    parent: null,
    toggle: true
  };
  const DefaultType$a = {
    parent: '(null|element)',
    toggle: 'boolean'
  };

  /**
   * Class definition
   */

  class Collapse extends BaseComponent {
/**
* @description This function is the constructor for an accordion element. It initializes
* the accordion's child elements and sets up event listeners for toggling the
* visibility of the content.
* 
* @param { object } element - The `element` input parameter is used to pass the
* current element that the collapsible instance is being initialized on.
* 
* @param { object } config - The `config` input parameter provides configuration
* options for the collapsible component. It is an object that can contain properties
* such as `parent`, `toggle`, and other custom configurations that might be needed
* for the specific use case.
* 
* @returns { object } The output of this function is a set of elements that have
* been transformed and manipulated based on the provided configuration and state.
* The function takes an `element` and a `config` object as input and returns nothing
* (void). However. it modifies the `element` and its children by adding classes and
* attributes for accessibility and collapse/expand behavior.
*/
    constructor(element, config) {
      super(element, config);
      this._isTransitioning = false;
      this._triggerArray = [];
      const toggleList = SelectorEngine.find(SELECTOR_DATA_TOGGLE$4);
      for (const elem of toggleList) {
        const selector = SelectorEngine.getSelectorFromElement(elem);
        const filterElement = SelectorEngine.find(selector).filter(foundElement => foundElement === this._element);
        if (selector !== null && filterElement.length) {
          this._triggerArray.push(elem);
        }
      }
      this._initializeChildren();
      if (!this._config.parent) {
        this._addAriaAndCollapsedClass(this._triggerArray, this._isShown());
      }
      if (this._config.toggle) {
        this.toggle();
      }
    }

    // Getters
/**
* @description This function is a `static` getter method named `Default` that returns
* the value of a constant variable named `Default$a`.
* 
* @returns { object } The function returns `Default$a`.
*/
    static get Default() {
      return Default$a;
    }
/**
* @description This function returns the `DefaultType` constant which is defined as
* `$a`.
* 
* @returns { string } The output of this function is `DefaultType$a`.
*/
    static get DefaultType() {
      return DefaultType$a;
    }
/**
* @description The function defines a static method called `NAME` that returns the
* value of the field `NAME$b`.
* 
* @returns { string } The function `getName()` returns `NAME$b`, which is `null`.
* The reason is that the `NAME` variable is not defined and the `$b` suffix tries
* to reference a non-existent property.
*/
    static get NAME() {
      return NAME$b;
    }

    // Public
/**
* @description The `toggle()` function flips the visibility of an object between
* hide and show based on its current state.
* 
* @returns {  } This function "toggle" takes no arguments and simply returns the
* current value of the flag "_isShown".
* 
* When called on an object with _isShown = true (i.e., the widget is currently shown),
* the function will set _isShown = false and return false.
* 
* When called on an object with _isShown = false (i.e., the widget is currently
* hidden), the function will set _isShown = true and return true.
*/
    toggle() {
      if (this._isShown()) {
        this.hide();
      } else {
        this.show();
      }
    }
/**
* @description This function is the show() method of the Collapse widget.
* 
* @returns {  } Based on the code snippet provided:
* 
* The output returned by `show()` is undefined.
* 
* Here's a brief explanation of why:
* 
* 1/ The function starts by checking if the collapse is already transitioning or
* shown. If either of those conditions are true (i.e., `_isTransitioning` or
* `_isShown()` is true), the function returns without doing anything.
* 2/ Next. It finds the active children of the collapse (i.e., the ones that are not
* collapsed). It then loops through each active child and calls `hide()` on it.
* 3/ After that's done (and all active children have been hidden), the function
* prepares for the show animation by adding the class names ` Collapsing` and `show-$7`.
* 4/ It then triggers the `SHOW` event on the element.
* 5/ Finally: The function sets up the `complete` callback that will be called when
* the transition is complete. The `complete` callback will remove the ` Collapsing`
* class name and add the `SHOW` class name. It also will trigger the `SHOWN` event
* on the element.
* 
* In conclusion: The output of the `show()` function is undefined because it returns
* immediately if the collapse is already shown or transitioning.
*/
    show() {
      if (this._isTransitioning || this._isShown()) {
        return;
      }
      let activeChildren = [];

      // find active children
      if (this._config.parent) {
        activeChildren = this._getFirstLevelChildren(SELECTOR_ACTIVES).filter(element => element !== this._element).map(element => Collapse.getOrCreateInstance(element, {
          toggle: false
        }));
      }
      if (activeChildren.length && activeChildren[0]._isTransitioning) {
        return;
      }
      const startEvent = EventHandler.trigger(this._element, EVENT_SHOW$6);
      if (startEvent.defaultPrevented) {
        return;
      }
      for (const activeInstance of activeChildren) {
        activeInstance.hide();
      }
      const dimension = this._getDimension();
      this._element.classList.remove(CLASS_NAME_COLLAPSE);
      this._element.classList.add(CLASS_NAME_COLLAPSING);
      this._element.style[dimension] = 0;
      this._addAriaAndCollapsedClass(this._triggerArray, true);
      this._isTransitioning = true;
/**
* @description This function "complete" completes the collapse of a collapsible element.
* 
* @returns {  } The function takes no arguments and has no returns statement. Instead
* it modifies the state of an object and triggers an event.
* 
* The function sets `this._isTransitioning` to false and adds classes `CLASS_NAME_COLLAPSE`
* and `CLASS_NAME_SHOW$7` to the element. It also removes any existing values from
* the `dimension` style property.
*/
      const complete = () => {
        this._isTransitioning = false;
        this._element.classList.remove(CLASS_NAME_COLLAPSING);
        this._element.classList.add(CLASS_NAME_COLLAPSE, CLASS_NAME_SHOW$7);
        this._element.style[dimension] = '';
        EventHandler.trigger(this._element, EVENT_SHOWN$6);
      };
      const capitalizedDimension = dimension[0].toUpperCase() + dimension.slice(1);
      const scrollSize = `scroll${capitalizedDimension}`;
      this._queueCallback(complete, this._element, true);
      this._element.style[dimension] = `${this._element[scrollSize]}px`;
    }
/**
* @description The function `hide` performs the following actions:
* 
* 1/ Checks if the element is currently hiding or not.
* 2/ Triggers an event to allow handlers to cancel the hide animation.
* 3/ Sets the dimensions of the element based on its current bounding client rect.
* 4/ Adds the `classNameCollapsing` class to the element and removes the `ClassNameShow`
* and `ClassNameCollapse` classes.
* 5/ Iterates through an array of trigger selectors and adds/removes the `aria-expanded`
* attribute and `classNameCollapsed` class based on the element's visibility.
* 6/ Starts a transition by setting the transition property of the element's style
* to the corresponding dimension.
* 7/ After the transition is completed (as determined by the `isTransitioning` flag),
* it will add the `ClassNameCollapse` class and remove the `ClassNameCollapsing`
* class from the element.
* 8/ Finally triggers an event indicating that the element is hidden (`EventHandler.trigger(this._element，EVENT_HIDDEN$6)`).
* 
* @returns {  } The `hide` function is a utility function for hiding an element with
* animation. It does the following:
* 
* 1/ If the element is not shown or transitioning yet (i.e., already hidden), return
* immediately.
* 2/ Trigger an `EVENT_HIDE$6` event on the element to allow handlers to abort the
* transition.
* 3/ If the `defaultPrevented` property of the `Event` object is set to `true`,
* return immediately.
* 4/ Get the current dimension (width or height) of the element.
* 5/ Set the CSS property for that dimension to the current value minus the margin
* and padding.
* 6/ Call `reflow` on the element to ensure the new dimensions are applied properly.
* 7/ Add the `CLASS_NAME_COLLAPSING` class to the element to start the collapse animation.
* 8/ Remove the `CLASS_NAME_COLLAPSE` and `CLASS_NAME_SHOW$7` classes from the element.
* 9/ For each trigger element that was specified when creating the accordion container
* instance (using `_triggerArray`), add or remove the `aria-hidden` attribute based
* on whether the element is shown or hidden.
* 10/ Set the `isTransitioning` property to `true`.
* 11/ Perform a transition by setting the CSS property for the dimension to an empty
* string and then calling the `complete` function when the transition is finished.
*/
    hide() {
      if (this._isTransitioning || !this._isShown()) {
        return;
      }
      const startEvent = EventHandler.trigger(this._element, EVENT_HIDE$6);
      if (startEvent.defaultPrevented) {
        return;
      }
      const dimension = this._getDimension();
      this._element.style[dimension] = `${this._element.getBoundingClientRect()[dimension]}px`;
      reflow(this._element);
      this._element.classList.add(CLASS_NAME_COLLAPSING);
      this._element.classList.remove(CLASS_NAME_COLLAPSE, CLASS_NAME_SHOW$7);
      for (const trigger of this._triggerArray) {
        const element = SelectorEngine.getElementFromSelector(trigger);
        if (element && !this._isShown(element)) {
          this._addAriaAndCollapsedClass([trigger], false);
        }
      }
      this._isTransitioning = true;
/**
* @description This function sets the `CLASS_NAME_COLLAPSING` class on the element
* to `CLASS_NAME_COLLAPSE`, triggers an event indicating the element has been hidden
* and sets `this._isTransitioning` to false
* 
* @returns { any } The output of the `complete` function is:
* 
* 	- `this._isTransitioning = false;` - sets a private flag to `false` indicating
* that the transition has completed.
* 	- `this._element.classList.remove(CLASS_NAME_COLLAPSING);` - removes the "collapsing"
* class from the element.
* 	- `this._element.classList.add(CLASS_NAME_COLLAPSE);` - adds the "collapse" class
* to the element.
* 	- `EventHandler.trigger(this._element , EVENT_HIDDEN$6)` - triggers the `hidden`
* event on the element.
* 
* In concise terms: the function completes the collapse transition and notifies the
* component that the transition has finished.
*/
      const complete = () => {
        this._isTransitioning = false;
        this._element.classList.remove(CLASS_NAME_COLLAPSING);
        this._element.classList.add(CLASS_NAME_COLLAPSE);
        EventHandler.trigger(this._element, EVENT_HIDDEN$6);
      };
      this._element.style[dimension] = '';
      this._queueCallback(complete, this._element, true);
    }
/**
* @description This function checks whether an element has a class name equal to `CLASS_NAME_SHOW$7`.
* 
* @param {  } element - The `element` input parameter is optional and defaults to `this._element`.
* 
* @returns { boolean } The function `_isShown()` takes an optional parameter `element`
* and returns a boolean value indicating whether the element has the class `CLASS_NAME_SHOW$.7`.
*/
    _isShown(element = this._element) {
      return element.classList.contains(CLASS_NAME_SHOW$7);
    }

    // Private
/**
* @description This function modifies the `config` object by coercing string values
* to Booleans and setting the `parent` property to an Element using `get element()`
* method.
* 
* @param { object } config - The `config` input parameter is a configuration object
* that contains properties such as `toggle` and `parent`.
* 
* @returns { object } This function takes a configuration object `config` as input
* and returns a new configuration object with two properties: `toggle` and `parent`.
* Here's a brief description of the output returned by this function:
* 
* 	- The `toggle` property is set to a boolean value (either `true` or `false`) based
* on the input value. If the input value is a string ("true" or "false"), it is
* coerced to a boolean value.
* 	- The `parent` property is set to the result of calling the `getElement` function
* with the `config.parent` value as input.
*/
    _configAfterMerge(config) {
      config.toggle = Boolean(config.toggle); // Coerce string values
      config.parent = getElement(config.parent);
      return config;
    }
/**
* @description This function returns the current dimensions of the element based on
* its class list.
* 
* @returns { number } The function `_getDimension()` returns either `WIDTH` or
* `HEIGHT`, depending on whether the element has the class `CLASS_NAME_HORIZONTAL`
* or not.
*/
    _getDimension() {
      return this._element.classList.contains(CLASS_NAME_HORIZONTAL) ? WIDTH : HEIGHT;
    }
/**
* @description This function iterates over the first-level children of an element
* and adds aria-expanded and collapsed classes to them based on their show/hide state.
* 
* @returns { array } The output of this function is not explicitly defined since it
* is a method and not a value. However based on the function name `_initializeChildren`
* we can infer that the function prepares the child elements of the component by
* adding ARIA and collapsed classes to them. Additionally the function appears to
* select first level children with the selector `SELECTOR_DATA_TOGGLE$4` and iterate
* through each child element.
*/
    _initializeChildren() {
      if (!this._config.parent) {
        return;
      }
      const children = this._getFirstLevelChildren(SELECTOR_DATA_TOGGLE$4);
      for (const element of children) {
        const selected = SelectorEngine.getElementFromSelector(element);
        if (selected) {
          this._addAriaAndCollapsedClass([element], this._isShown(selected));
        }
      }
    }
/**
* @description The `getFirstLevelChildren` function finds the direct children of an
* element that match a given selector and return only those children with the specified
* class name (CLASS_NAME_DEEPER_CHILDREN), excluding any deeper child elements that
* also match the selector.
* 
* @param { string } selector - The `selector` parameter is a string that represents
* the selector to be applied to the elements to find the first-level children.
* 
* @returns { object } The function `_getFirstLevelChildren` returns an array of
* elements that match the provided `selector` and are direct children of the parent
* element (i.e., they have no other children), excluding any children that have a
* deeper depth (as determined by the `SelectorEngine.find` method).
*/
    _getFirstLevelChildren(selector) {
      const children = SelectorEngine.find(CLASS_NAME_DEEPER_CHILDREN, this._config.parent);
      // remove children if greater depth
      return SelectorEngine.find(selector, this._config.parent).filter(element => !children.includes(element));
    }
/**
* @description This function adds the `aria-expanded` attribute and two CSS classes
* (` className_name_collapsed` and `className_name_expanded`) to an array of elements
* (triggers), depending on a boolean parameter (isOpen).
* 
* @param { array } triggerArray - The `triggerArray` input parameter is an array of
* elements that are used to toggle the collapse state.
* 
* @param { boolean } isOpen - The `isOpen` input parameter controls whether the panel
* should be set to "true" (meaning open) or "false" (meaning collapsed).
* 
* @returns {  } This function takes an array of elements and a boolean flag indicating
* whether the content should be expanded or collapsed.
*/
    _addAriaAndCollapsedClass(triggerArray, isOpen) {
      if (!triggerArray.length) {
        return;
      }
      for (const element of triggerArray) {
        element.classList.toggle(CLASS_NAME_COLLAPSED, !isOpen);
        element.setAttribute('aria-expanded', isOpen);
      }
    }

    // Static
/**
* @description This function is a JavaScript function called `jQueryInterface` that
* extends the jQuery interface for Collapse widgets. It takes an object configuration
* `config` and performs the following actions:
* 
* 1/ Toggles the visibility of the Collapse instance based on the `config` parameter.
* 
* @param { object } config - The `config` input parameter allows you to pass custom
* options for the Collapse instance being created or updated. It can be a string or
* an object and is used to toggle the visibility of the collapse element. If it's a
* string and matches either "show" or "hide", it will toggle the visibility of the
* element.
* 
* @returns { object } The function `jQueryInterface` returns a `this` object that
* has been iterated over each element with a given Collapse instance. The function
* accepts two parameters: `config` and `this`. The return value is not explicitly
* stated but it returns a value of the iteration done to each object using `this.each`.
*/
    static jQueryInterface(config) {
      const _config = {};
      if (typeof config === 'string' && /show|hide/.test(config)) {
        _config.toggle = false;
      }
      return this.each(function () {
        const data = Collapse.getOrCreateInstance(this, _config);
        if (typeof config === 'string') {
          if (typeof data[config] === 'undefined') {
            throw new TypeError(`No method named "${config}"`);
          }
          data[config]();
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$4, SELECTOR_DATA_TOGGLE$4, function (event) {
    // preventDefault only for <a> elements (which change the URL) not inside the collapsible element
    if (event.target.tagName === 'A' || event.delegateTarget && event.delegateTarget.tagName === 'A') {
      event.preventDefault();
    }
    for (const element of SelectorEngine.getMultipleElementsFromSelector(this)) {
      Collapse.getOrCreateInstance(element, {
        toggle: false
      }).toggle();
    }
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Collapse);

  var top = 'top';
  var bottom = 'bottom';
  var right = 'right';
  var left = 'left';
  var auto = 'auto';
  var basePlacements = [top, bottom, right, left];
  var start = 'start';
  var end = 'end';
  var clippingParents = 'clippingParents';
  var viewport = 'viewport';
  var popper = 'popper';
  var reference = 'reference';
  var variationPlacements = /*#__PURE__*/basePlacements.reduce(function (acc, placement) {
    return acc.concat([placement + "-" + start, placement + "-" + end]);
  }, []);
  var placements = /*#__PURE__*/[].concat(basePlacements, [auto]).reduce(function (acc, placement) {
    return acc.concat([placement, placement + "-" + start, placement + "-" + end]);
  }, []); // modifiers that need to read the DOM

  var beforeRead = 'beforeRead';
  var read = 'read';
  var afterRead = 'afterRead'; // pure-logic modifiers

  var beforeMain = 'beforeMain';
  var main = 'main';
  var afterMain = 'afterMain'; // modifier with the purpose to write to the DOM (or write into a framework state)

  var beforeWrite = 'beforeWrite';
  var write = 'write';
  var afterWrite = 'afterWrite';
  var modifierPhases = [beforeRead, read, afterRead, beforeMain, main, afterMain, beforeWrite, write, afterWrite];

/**
* @description The function `getNodeName` takes an `element` argument and returns
* its node name (i.e., the local name of the element) as a lowercase string.
* 
* @param {  } element - The `element` input parameter is optional and provides the
* DOM element whose node name should be retrieved.
* 
* @returns { string } The output returned by this function is a string representing
* the node name of the input element. If the element is null or does not have a node
* name (i.e., `element.nodeName` returns undefined), then the function returns null.
*/
  function getNodeName(element) {
    return element ? (element.nodeName || '').toLowerCase() : null;
  }

/**
* @description This function returns the window object related to a given node (or
* the current window if the node is null).
* 
* @param { object } node - The `node` input parameter is optional and can be null.
* 
* @returns { object } The output of this function is `window` regardless of the input
* node (even if it's null). This means that the function always returns the window
* object.
* 
* Here's a breakdown of the function:
* 
* 1/ If the input node is null or undefined (i.e., `node == null`), the function
* returns `window`.
* 2/ Otherwise (if `node` is not null), it checks if `node` is a window object by
* checking its `toString()` method.
*/
  function getWindow(node) {
    if (node == null) {
      return window;
    }

    if (node.toString() !== '[object Window]') {
      var ownerDocument = node.ownerDocument;
      return ownerDocument ? ownerDocument.defaultView || window : window;
    }

    return node;
  }

/**
* @description This function checks if a given `node` is an element or not.
* 
* @param {  } node - The `node` input parameter is the object that you want to check
* if it's an element or not.
* 
* @returns { boolean } The function `isElement` takes a Node object `node` as an
* argument and returns a boolean value indicating whether `node` is an HTML element
* or not.
* 
* The function first retrieves the `Element` object from the global scope (using
* `getWindow(node).Element`), and then checks if `node` is either an instance of the
* `Element` object or a node that has an `ownerDocument` property set to the `Element`
* object.
* 
* Therefore the output returned by this function is a boolean value that indicates
* whether `node` is an HTML element or not.
*/
  function isElement(node) {
    var OwnElement = getWindow(node).Element;
    return node instanceof OwnElement || node instanceof Element;
  }

/**
* @description This function checks if a given `node` is an HTML element or not. It
* uses the `getWindow()` method to get the current window object and then checks if
* `node` is an instance of that window's `HTMLElement` object.
* 
* @param { object } node - The `node` input parameter is a reference to a DOM element
* and the function checks if it's an HTML element or not.
* 
* @returns { boolean } The function `isHTMLElement` takes a Node object as input and
* returns a boolean value indicating whether the given Node is an HTML element or not.
*/
  function isHTMLElement(node) {
    var OwnElement = getWindow(node).HTMLElement;
    return node instanceof OwnElement || node instanceof HTMLElement;
  }

/**
* @description This function checks if a given DOM element is a shadow root or one
* of its descendants.
* 
* @param {  } node - The `node` input parameter is used to check if a given DOM
* element has a shadow root.
* 
* @returns { boolean } The output returned by this function is a boolean value that
* indicates whether the provided `node` object is a shadow root or not.
*/
  function isShadowRoot(node) {
    // IE 11 has no ShadowRoot
    if (typeof ShadowRoot === 'undefined') {
      return false;
    }

    var OwnElement = getWindow(node).ShadowRoot;
    return node instanceof OwnElement || node instanceof ShadowRoot;
  }

  // and applies them to the HTMLElements such as popper and arrow

/**
* @description This function takes an object with state properties `styles` and
* `attributes` for each Element's style and attributes respectively.
* 
* @param { object } _ref - The `_ref` parameter is an object that contains the `state`
* of the application.
* 
* @returns { object } The `applyStyles` function takes an object `_ref` with a `state`
* property that contains two properties: `styles` and `attributes`. The function
* iterates over the elements stored at `state.elements` and applies the styles defined
* at `state.styles` for each element.
* 
* The output of the function is not explicitly returned. Instead., it mutates the
* DOM by setting properties like `style` and attributes on the elements passed to it.
*/
  function applyStyles(_ref) {
    var state = _ref.state;
    Object.keys(state.elements).forEach(function (name) {
      var style = state.styles[name] || {};
      var attributes = state.attributes[name] || {};
      var element = state.elements[name]; // arrow is optional + virtual elements

      if (!isHTMLElement(element) || !getNodeName(element)) {
        return;
      } // Flow doesn't support to extend this property, but it's the most
      // effective way to apply styles to an HTMLElement
      // $FlowFixMe[cannot-write]


      Object.assign(element.style, style);
      Object.keys(attributes).forEach(function (name) {
        var value = attributes[name];

        if (value === false) {
          element.removeAttribute(name);
        } else {
          element.setAttribute(name, value === true ? '' : value);
        }
      });
    });
  }

/**
* @description This function initializes and unsets styles for a Popper.js component's
* popper and arrow elements. It sets the position of the popper element based on the
* strategy option passed down from the parent component.
* 
* @param { object } _ref2 - The `_ref2` input parameter is used to pass the `state`
* object down to the function. It is an optional parameter that is provided by the
* calling code and contains the current state of thePopper library's internal data.
* 
* @returns {  } The output returned by this function is a function that unsets all
* styles and attributes for each Popper.js element. It does this by iterating over
* the `state.elements` object and applying the `style` and `attributes` properties
* from the `initialStyles` object to each element. If an element is not an HTMLElement
* or has no `NodeName`, it is skipped.
*/
  function effect$2(_ref2) {
    var state = _ref2.state;
    var initialStyles = {
      popper: {
        position: state.options.strategy,
        left: '0',
        top: '0',
        margin: '0'
      },
      arrow: {
        position: 'absolute'
      },
      reference: {}
    };
    Object.assign(state.elements.popper.style, initialStyles.popper);
    state.styles = initialStyles;

    if (state.elements.arrow) {
      Object.assign(state.elements.arrow.style, initialStyles.arrow);
    }

    return function () {
      Object.keys(state.elements).forEach(function (name) {
        var element = state.elements[name];
        var attributes = state.attributes[name] || {};
        var styleProperties = Object.keys(state.styles.hasOwnProperty(name) ? state.styles[name] : initialStyles[name]); // Set all values to an empty string to unset them

        var style = styleProperties.reduce(function (style, property) {
          style[property] = '';
          return style;
        }, {}); // arrow is optional + virtual elements

        if (!isHTMLElement(element) || !getNodeName(element)) {
          return;
        }

        Object.assign(element.style, style);
        Object.keys(attributes).forEach(function (attribute) {
          element.removeAttribute(attribute);
        });
      });
    };
  } // eslint-disable-next-line import/no-unused-modules


  const applyStyles$1 = {
    name: 'applyStyles',
    enabled: true,
    phase: 'write',
    fn: applyStyles,
    effect: effect$2,
    requires: ['computeStyles']
  };

/**
* @description This function takes a string representing a placement (e.g. "top-right")
* and returns the base placement (e.g.
* 
* @param { string } placement - The `placement` input parameter is a string that
* represents a complete placement identifier (e.g.
* 
* @returns { array } The output returned by the function `getBasePlacement` is the
* first word of the string passed as an argument to the function. This is achieved
* by using the `split()` method to split the input string on the '-' character and
* then taking the first element of the resulting array.
*/
  function getBasePlacement(placement) {
    return placement.split('-')[0];
  }

  var max = Math.max;
  var min = Math.min;
  var round = Math.round;

/**
* @description The provided function retrieves the user agent string from the navigator
* object and returns a concatenated string of the brand and version information
* extracted from the user agent data.
* 
* @returns { string } The function `getUAString()` returns a string representing the
* User Agent (UA) of the system's browser. It does this by extracting the brand and
* version information from the `navigator.userAgentData` object if available or using
* the entire `navigator.userAgent` string as fallback.
* 
* The output is a concatenation of brand names and version numbers separated by spaces.
*/
  function getUAString() {
    var uaData = navigator.userAgentData;

    if (uaData != null && uaData.brands && Array.isArray(uaData.brands)) {
      return uaData.brands.map(function (item) {
        return item.brand + "/" + item.version;
      }).join(' ');
    }

    return navigator.userAgent;
  }

/**
* @description This function checks whether the current device is a Safari browser
* on a desktop device (i.e., not Chrome or Android) based on the User Agent string.
* 
* @returns { boolean } This function takes no arguments and returns a boolean value
* indicating whether the current device is a layout viewport or not.
*/
  function isLayoutViewport() {
    return !/^((?!chrome|android).)*safari/i.test(getUAString());
  }

/**
* @description This function gets the bounding client rect of an element and returns
* it with scaled coordinates taking into account fixed strategies and visual viewports.
* 
* @param { object } element - The `element` input parameter is the HTML element whose
* bounding client rect should be retrieved and returned as an object.
* 
* @param { boolean } includeScale - The `includeScale` parameter determines whether
* to include the element's scaling factor (width and height) when calculating the
* bounding client rect.
* 
* @param { boolean } isFixedStrategy - The `isFixedStrategy` parameter controls
* whether the method includes visual viewport offsets when computing the bounding
* client rect.
* 
* @returns { object } The output returned by this function is an object with six
* properties: `width`, `height`, `top`, `right`, `bottom`, and `left`. These properties
* represent the bounding rectangular coordinates of an HTML element with scaling
* consideration taken into account. Specifically:
* 
* 	- `width` and `height` represent the actual width and height of the element.
* 	- `top`, `right`, `bottom`, and `left` represent the coordinate offsets of the
* element from its containing block's top left corner.
* 
* The function returns these coordinates scaled by the element's size and the current
* visual viewport's offset values if `includeScale` is set to true and the element
* is an HTML element.
*/
  function getBoundingClientRect(element, includeScale, isFixedStrategy) {
    if (includeScale === void 0) {
      includeScale = false;
    }

    if (isFixedStrategy === void 0) {
      isFixedStrategy = false;
    }

    var clientRect = element.getBoundingClientRect();
    var scaleX = 1;
    var scaleY = 1;

    if (includeScale && isHTMLElement(element)) {
      scaleX = element.offsetWidth > 0 ? round(clientRect.width) / element.offsetWidth || 1 : 1;
      scaleY = element.offsetHeight > 0 ? round(clientRect.height) / element.offsetHeight || 1 : 1;
    }

    var _ref = isElement(element) ? getWindow(element) : window,
        visualViewport = _ref.visualViewport;

    var addVisualOffsets = !isLayoutViewport() && isFixedStrategy;
    var x = (clientRect.left + (addVisualOffsets && visualViewport ? visualViewport.offsetLeft : 0)) / scaleX;
    var y = (clientRect.top + (addVisualOffsets && visualViewport ? visualViewport.offsetTop : 0)) / scaleY;
    var width = clientRect.width / scaleX;
    var height = clientRect.height / scaleY;
    return {
      width: width,
      height: height,
      top: y,
      right: x + width,
      bottom: y + height,
      left: x,
      x: x,
      y: y
    };
  }

  // means it doesn't take into account transforms.

/**
* @description This function gets the bounding box of an element and returns it with
* modified width and height values to account for padding and scroll positions.
* 
* @param {  } element - The `element` input parameter is passed as a reference to
* an HTML element.
* 
* @returns { object } The output returned by the `getLayoutRect` function is an
* object with properties for `x`, `y`, `width`, and `height`.
*/
  function getLayoutRect(element) {
    var clientRect = getBoundingClientRect(element); // Use the clientRect sizes if it's not been transformed.
    // Fixes https://github.com/popperjs/popper-core/issues/1223

    var width = element.offsetWidth;
    var height = element.offsetHeight;

    if (Math.abs(clientRect.width - width) <= 1) {
      width = clientRect.width;
    }

    if (Math.abs(clientRect.height - height) <= 1) {
      height = clientRect.height;
    }

    return {
      x: element.offsetLeft,
      y: element.offsetTop,
      width: width,
      height: height
    };
  }

/**
* @description This function checks if a child element is a descendant of a given
* parent element using two different methods:
* 
* 1/ Firstly it tries to use the `contains` method provided by the parent element.
* 2/ If that fails (i.e., the `contains` method is not supported or the element is
* not a descendant), it falls back to a custom implementation that uses the Shadow
* DOM.
* 3/ In the case of the Shadow DOM implementation: it iterates up the parent chain
* looking for a match starting from the child element and checks if the parent element
* is the same as the current element until it reaches the top of the Shadow DOM or
* the parent element is found.
* 
* In conclusion the function returns `true` if the child is a descendant of the
* parent else `false`.
* 
* @param {  } parent - The `parent` input parameter represents the parent element
* of the `child` element to be searched.
* 
* @param {  } child - In this function `contains`, the `child` parameter is the
* element that we want to check if it is a descendant of the `parent` element.
* 
* @returns { boolean } The output of this function is a boolean value indicating
* whether the parent node contains the child node. The function first tries to use
* the faster native `contains()` method if available on the child node (represented
* by `child.getRootNode()`), and if that fails (i.e., the child node doesn't have a
* root node or the root node is not a shadow root), it falls back to a custom
* implementation that supports Shadow DOM. The custom implementation iterates up the
* parent node's hierarchy looking for the child node until it reaches the parent
* node itself (indicating that the child node is contained within the parent). If
* the iteration completes without finding the child node or if the root node is not
* a shadow root at any point during the iteration), the function returns `false`.
*/
  function contains(parent, child) {
    var rootNode = child.getRootNode && child.getRootNode(); // First, attempt with faster native method

    if (parent.contains(child)) {
      return true;
    } // then fallback to custom implementation with Shadow DOM support
    else if (rootNode && isShadowRoot(rootNode)) {
        var next = child;

        do {
          if (next && parent.isSameNode(next)) {
            return true;
          } // $FlowFixMe[prop-missing]: need a better way to handle this...


          next = next.parentNode || next.host;
        } while (next);
      } // Give up, the result is false


    return false;
  }

/**
* @description This function retrieves the computed style of an element.
* 
* @param { object } element - The `element` input parameter is passed by the caller
* as a reference to an HTML element and is used to retrieve the computed style
* properties of that specific element using the `getComputedStyle()` method provided
* by the window object.
* 
* @returns { object } The function `getComputedStyle$1` returns the computed style
* of an element as an object.
*/
  function getComputedStyle$1(element) {
    return getWindow(element).getComputedStyle(element);
  }

/**
* @description This function checks if the provided `element` is a table element
* (i.e., a `table`, `td`, or `th`) by checking if its node name is contained within
* the array `[ 'table', 'td', 'th' ]`.
* 
* @param { object } element - The `element` input parameter is passed to the
* `getNodeName()` function to retrieve the element's node name and then checked
* against an array of expected names (`['table', 'td', 'th']`) to determine if it
* is a table element.
* 
* @returns { boolean } The function takes an `element` parameter and returns a boolean
* value indicating whether the element is a table element or not. It does this by
* checking if the node name of the element is equal to "table", "td", or "th".
*/
  function isTableElement(element) {
    return ['table', 'td', 'th'].indexOf(getNodeName(element)) >= 0;
  }

/**
* @description This function retrieves the `DocumentElement` of an HTML element. It
* first checks if the passed `element` is an actual HTML element and if it has an
* `ownerDocument`. If notfound return undefined. Then returns the `documentElement`
* property from the `ownerDocument`, and if that fails to execute properly , falls
* back to the global `window.document`.
* 
* @param {  } element - The `element` input parameter is passed as a reference to
* an existing DOM element. The function uses this parameter to check if the element
* is already connected to a document by checking if it has an `ownerDocument` property
* or a `document` property.
* 
* @returns { object } The output of this function is the `documentElement` of the
* given `element`, which is either the current document element if `element` is an
* HTMLElement or the element's owner document's document element otherwise.
*/
  function getDocumentElement(element) {
    // $FlowFixMe[incompatible-return]: assume body is always available
    return ((isElement(element) ? element.ownerDocument : // $FlowFixMe[prop-missing]
    element.document) || window.document).documentElement;
  }

/**
* @description The function `getParentNode` returns the parent node of a given DOM
* element. It first checks if the element is the root HTML element and returns it
* if so. If not.
* 
* @param {  } element - The `element` input parameter is passed to the function and
* represents the DOM element for which the parent node needs to be determined.
* 
* @returns {  } The `getParentNode` function takes an `element` argument and returns
* the parent node of that element.
*/
  function getParentNode(element) {
    if (getNodeName(element) === 'html') {
      return element;
    }

    return (// this is a quicker (but less type safe) way to save quite some bytes from the bundle
      // $FlowFixMe[incompatible-return]
      // $FlowFixMe[prop-missing]
      element.assignedSlot || // step into the shadow DOM of the parent of a slotted node
      element.parentNode || ( // DOM Element detected
      isShadowRoot(element) ? element.host : null) || // ShadowRoot detected
      // $FlowFixMe[incompatible-call]: HTMLElement is a Node
      getDocumentElement(element) // fallback

    );
  }

/**
* @description This function determines the true offset parent of an HTML element
* by returning the first ancestor element with a non-zero offset position other than
* the root element.
* 
* @param {  } element - The `element` input parameter is passed to the function and
* it's used to specify which element the function should get the offset parent for.
* 
* @returns { object } The output returned by the `getTrueOffsetParent` function is
* the "true" offset parent of an HTML element.
* 
* In other words:
* 
* 	- If the input element is not an HTML element or its `position` property is set
* to `fixed`, the function returns `null`.
* 	- Otherwise (i.e., the element is an HTML element with a non-fixed position), the
* function returns the element's offset parent (i.e., the highest element that has
* an offset height/width and has a position other than `static`).
* 
* In simpler terms: if the element you start with has no offset parent or its position
* is set to fixed (i.e., it does not change position when the user scrolls), the
* function returns null.
*/
  function getTrueOffsetParent(element) {
    if (!isHTMLElement(element) || // https://github.com/popperjs/popper-core/issues/837
    getComputedStyle$1(element).position === 'fixed') {
      return null;
    }

    return element.offsetParent;
  } // `.offsetParent` reports `null` for fixed elements, while absolute elements
  // return the containing block


/**
* @description The `getContainingBlock()` function checks if an Element has a
* containing block and returns it if found or `null` otherwise.
* 
* @param { object } element - The `element` parameter is an HTMLElement object that
* represents the element for which you want to find its containing block.
* 
* @returns {  } This function takes an HTML element as input and returns the containing
* block element of that element or null if no such element exists.
*/
  function getContainingBlock(element) {
    var isFirefox = /firefox/i.test(getUAString());
    var isIE = /Trident/i.test(getUAString());

    if (isIE && isHTMLElement(element)) {
      // In IE 9, 10 and 11 fixed elements containing block is always established by the viewport
      var elementCss = getComputedStyle$1(element);

      if (elementCss.position === 'fixed') {
        return null;
      }
    }

    var currentNode = getParentNode(element);

    if (isShadowRoot(currentNode)) {
      currentNode = currentNode.host;
    }

    while (isHTMLElement(currentNode) && ['html', 'body'].indexOf(getNodeName(currentNode)) < 0) {
      var css = getComputedStyle$1(currentNode); // This is non-exhaustive but covers the most common CSS properties that
      // create a containing block.
      // https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block#identifying_the_containing_block

      if (css.transform !== 'none' || css.perspective !== 'none' || css.contain === 'paint' || ['transform', 'perspective'].indexOf(css.willChange) !== -1 || isFirefox && css.willChange === 'filter' || isFirefox && css.filter && css.filter !== 'none') {
        return currentNode;
      } else {
        currentNode = currentNode.parentNode;
      }
    }

    return null;
  } // Gets the closest ancestor positioned element. Handles some edge cases,
  // such as table ancestors and cross browser bugs.


/**
* @description This function `getOffsetParent` returns the nearest parent element
* that has a non-static position (i.e., `position: relative`, `position: absolute`,
* or `position: fixed`) and is not an HTML or BODY element.
* 
* @param {  } element - The `element` input parameter is the DOM element for which
* you want to find its offset parent.
* 
* @returns { object } This function takes an element as an argument and returns the
* offset parent of that element.
*/
  function getOffsetParent(element) {
    var window = getWindow(element);
    var offsetParent = getTrueOffsetParent(element);

    while (offsetParent && isTableElement(offsetParent) && getComputedStyle$1(offsetParent).position === 'static') {
      offsetParent = getTrueOffsetParent(offsetParent);
    }

    if (offsetParent && (getNodeName(offsetParent) === 'html' || getNodeName(offsetParent) === 'body' && getComputedStyle$1(offsetParent).position === 'static')) {
      return window;
    }

    return offsetParent || getContainingBlock(element) || window;
  }

/**
* @description This function takes a string representing a placement (e.g. "top",
* "bottom") and returns the main axis (x or y) based on the placement.
* 
* @param { string } placement - The `placement` input parameter is a string that
* determines the orientation of the main axis of the chart.
* 
* @returns { string } The output returned by the function `getMainAxisFromPlacement`
* is a string indicating the main axis (either 'x' or 'y') based on the value of the
* `placement` parameter.
* 
* The function takes a string parameter `placement`, and checks if it matches any
* of the values 'top' or 'bottom'.
*/
  function getMainAxisFromPlacement(placement) {
    return ['top', 'bottom'].indexOf(placement) >= 0 ? 'x' : 'y';
  }

/**
* @description The function takes three parameters `min$, `value`, and `max$`, and
* returns the largest of the following three values:
* 
* 	- `min$`
* 	- `value`
* 	- `max$`
* 
* In other words， the function Returns Max(Min(value), Min(max$, min$))
* 
* @param { number } min$1 - In the given function `within`, the `min$1` input parameter
* is not used anywhere and has no effect on the function's behavior.
* 
* @param { string } value - The `value` parameter is not used anywhere within the
* function `within`.
* 
* @param { number } max$1 - In the given function `within`, the `max$1` input parameter
* is not used at all. The function only uses the `min$1` and `value` parameters to
* calculate the returned value.
* 
* @returns { number } The output returned by the function `within(min$1、value、max$1)`
* is `min(min$1、value)`.
*/
  function within(min$1, value, max$1) {
    return max(min$1, min(value, max$1));
  }
/**
* @description This function limits a given value `value` to be within the range of
* `[min`, `max]`.
* 
* @param { number } min - The `min` input parameter specifies the minimum value that
* the `value` parameter can take.
* 
* @param { integer } value - The `value` parameter is the input value that needs to
* be clamped between `min` and `max`.
* 
* @param { number } max - The `max` input parameter sets the upper bound for the
* return value of the function.
* 
* @returns { number } The function `withinMaxClamp` takes three parameters: `min`,
* `value`, and `max`. It returns the value of `value` clamped within the range defined
* by `min` and `max`.
* 
* If `value` is greater than `max`, the function returns `max`. If `value` is less
* than or equal to `min`, the function returns `min`.
*/
  function withinMaxClamp(min, value, max) {
    var v = within(min, value, max);
    return v > max ? max : v;
  }

/**
* @description This function returns an object with the values `top`, `right`,
* `bottom`, and `left` all set to zero.
* 
* @returns { object } The function `getFreshSideObject()` returns an object with all
* its properties set to `0`, such as:
* 
* {
* top: 0
* right: 0
* bottom: 0
* left: 0
* }
* 
* In other words、it returns an empty object.
*/
  function getFreshSideObject() {
    return {
      top: 0,
      right: 0,
      bottom: 0,
      left: 0
    };
  }

/**
* @description This function takes an object `paddingObject` and returns a new object
* that merges the contents of `paddingObject` with a fresh copy of an empty object
* `getFreshSideObject()`.
* 
* @param { object } paddingObject - The `paddingObject` input parameter is passed
* as an object and its purpose is to provide the additional properties or values
* that should be merged with the resulting fresh side object.
* 
* @returns { object } The output returned by the `mergePaddingObject` function is
* an object that contains all the properties of the `paddingObject` argument and
* additionally includes the properties from the `getFreshSideObject` function. In
* other words , it merges the two objects .
* 
* The function uses the `Object.assign` method to create a new object and merge the
* properties from the `paddingObject` and the `getFreshSideObject`.
*/
  function mergePaddingObject(paddingObject) {
    return Object.assign({}, getFreshSideObject(), paddingObject);
  }

/**
* @description This function takes a `value` and an `array of strings` as inputs and
* returns a `hashmap` with the value associated with each string key.
* 
* @param { any } value - The `value` input parameter is used to set the value
* associated with each key.
* 
* @param { array } keys - In the given function `expandToHashMap()`, the `keys` input
* parameter is an array of strings that represents the keys to be used as property
* names for the returned object.
* 
* @returns { object } The output of the function `expandToHashMap` is an object that
* maps the keys to the provided value. The function takes a value and a list of keys
* as inputs and returns a map where each key-value pair is created by pairing the
* key with the provided value.
* 
* In other words.
*/
  function expandToHashMap(value, keys) {
    return keys.reduce(function (hashMap, key) {
      hashMap[key] = value;
      return hashMap;
    }, {});
  }

/**
* @description The function `toPaddingObject` takes a padding object or function and
* returns a new padding object with the properties from the original object or
* function and any additional properties from the `state` object.
* 
* @param { object } padding - The `padding` input parameter specifies a padding value
* that is used to augment the default placements defined by the state object.
* 
* @param { object } state - The `state` input parameter is passed from a parent scope
* and is used to customize the returned padding object by merging it with an existing
* rectangle or placement data.
* 
* @returns { object } The `toPaddingObject` function takes a `padding` argument and
* an optional `state` argument. If the `padding` argument is a function or a map-like
* object (e.g., an array or an object with string keys), it returns the result of
* applying the `padding` function to an Object.assign of the current state's rectangles
* and the given placement.
*/
  var toPaddingObject = function toPaddingObject(padding, state) {
    padding = typeof padding === 'function' ? padding(Object.assign({}, state.rects, {
      placement: state.placement
    })) : padding;
    return mergePaddingObject(typeof padding !== 'number' ? padding : expandToHashMap(padding, basePlacements));
  };

/**
* @description This function prepares the arrow markup of a popper object to ensure
* it is correctly positioned relative to the reference element.
* 
* @param { object } _ref - The `_ref` input parameter is a reference object that
* contains information about the current state of the Popper.js instance.
* 
* @returns { object } The function takes four arguments: `state`, `name`, `options`,
* and `referenceRect`, and returns an object with two properties: `centerOffset` and
* `offset`.
* 
* Here's a concise description of the output:
* 
* The function calculates the center offset for an arrow element relative to its
* parent container. The `centerOffset` property represents the horizontal or vertical
* distance between the center of the arrow and the center of the popper reference rectangle.
*/
  function arrow(_ref) {
    var _state$modifiersData$;

    var state = _ref.state,
        name = _ref.name,
        options = _ref.options;
    var arrowElement = state.elements.arrow;
    var popperOffsets = state.modifiersData.popperOffsets;
    var basePlacement = getBasePlacement(state.placement);
    var axis = getMainAxisFromPlacement(basePlacement);
    var isVertical = [left, right].indexOf(basePlacement) >= 0;
    var len = isVertical ? 'height' : 'width';

    if (!arrowElement || !popperOffsets) {
      return;
    }

    var paddingObject = toPaddingObject(options.padding, state);
    var arrowRect = getLayoutRect(arrowElement);
    var minProp = axis === 'y' ? top : left;
    var maxProp = axis === 'y' ? bottom : right;
    var endDiff = state.rects.reference[len] + state.rects.reference[axis] - popperOffsets[axis] - state.rects.popper[len];
    var startDiff = popperOffsets[axis] - state.rects.reference[axis];
    var arrowOffsetParent = getOffsetParent(arrowElement);
    var clientSize = arrowOffsetParent ? axis === 'y' ? arrowOffsetParent.clientHeight || 0 : arrowOffsetParent.clientWidth || 0 : 0;
    var centerToReference = endDiff / 2 - startDiff / 2; // Make sure the arrow doesn't overflow the popper if the center point is
    // outside of the popper bounds

    var min = paddingObject[minProp];
    var max = clientSize - arrowRect[len] - paddingObject[maxProp];
    var center = clientSize / 2 - arrowRect[len] / 2 + centerToReference;
    var offset = within(min, center, max); // Prevents breaking syntax highlighting...

    var axisProp = axis;
    state.modifiersData[name] = (_state$modifiersData$ = {}, _state$modifiersData$[axisProp] = offset, _state$modifiersData$.centerOffset = offset - center, _state$modifiersData$);
  }

/**
* @description This function sets up the element representing the arrow that appears
* when a Popper.js component is expanded.
* 
* @param { object } _ref2 - The `_ref2` parameter is an object that contains `state`
* and `options` properties that are passed to the function. The `state` property
* contains information about the current state of the element being managed by Popper.js.
* 
* @returns { object } The output returned by this function is `undefined`.
* 
* The function takes an object with a `state` property and an `options` property.
* It extracts some properties from the `options` object (namely `element`) and then
* uses those properties to identify an arrow element that should be selected.
*/
  function effect$1(_ref2) {
    var state = _ref2.state,
        options = _ref2.options;
    var _options$element = options.element,
        arrowElement = _options$element === void 0 ? '[data-popper-arrow]' : _options$element;

    if (arrowElement == null) {
      return;
    } // CSS selector


    if (typeof arrowElement === 'string') {
      arrowElement = state.elements.popper.querySelector(arrowElement);

      if (!arrowElement) {
        return;
      }
    }

    if (!contains(state.elements.popper, arrowElement)) {
      return;
    }

    state.elements.arrow = arrowElement;
  } // eslint-disable-next-line import/no-unused-modules


  const arrow$1 = {
    name: 'arrow',
    enabled: true,
    phase: 'main',
    fn: arrow,
    effect: effect$1,
    requires: ['popperOffsets'],
    requiresIfExists: ['preventOverflow']
  };

/**
* @description The function `getVariation` takes a `placement` string and returns
* the second segment (after the dash) of the string.
* 
* @param { string } placement - The `placement` input parameter splits on a dash
* (`-`) and returns the second element of the array (i.e., the variation).
* 
* @returns { string } The function `getVariation` takes a string `placement` as input
* and returns the second element of the array obtained by splitting the `placement`
* string using the `-` character.
* 
* In other words., if we pass a string like "left-variant1" as the argument to the
* `getVariation` function，it will return the word "variant1".
*/
  function getVariation(placement) {
    return placement.split('-')[1];
  }

  var unsetSides = {
    top: 'auto',
    right: 'auto',
    bottom: 'auto',
    left: 'auto'
  }; // Round the offsets to the nearest suitable subpixel based on the DPR.
  // Zooming can change the DPR, but it seems to report a value that will
  // cleanly divide the values into the appropriate subpixels.

/**
* @description The function `roundOffsetsByDPR` takes two arguments `_ref` and `win`,
* and returns an object with two properties: `x` and `y`.
* 
* @param { object } _ref - The `_ref` input parameter is a reference to an object
* with `x` and `y` properties that contain the original offsets to be rounded.
* 
* @param { object } win - The `win` input parameter is not used within the function
* body of `roundOffsetsByDPR`. Therefore it can be safely ignored.
* 
* @returns { object } This function takes two arguments `_ref` and `win`, and returns
* an object with two properties: `x` and `y`.
*/
  function roundOffsetsByDPR(_ref, win) {
    var x = _ref.x,
        y = _ref.y;
    var dpr = win.devicePixelRatio || 1;
    return {
      x: round(x * dpr) / dpr || 0,
      y: round(y * dpr) / dpr || 0
    };
  }

/**
* @description This function maps styles for a Popper component based on the placement
* of the popper relative to its reference element. It calculates the sides
* (top/bottom/left/right) of the popper based on the placement and variation of the
* popper. It also accounts for gpu acceleration and adaptive placement.
* 
* @param { object } _ref2 - The `_ref2` input parameter is an object that contains
* various properties related to the positioning of the popper. It includes `popper`,
* `popperRect`, `placement`, `variation`, `offsets`, `position`, `gpuAcceleration`,
* `adaptive`, and `roundOffsets`.
* 
* @returns { object } This function takes an object with various properties related
* to a popper element and returns an object of CSS styles that can be applied to
* thepopper element to position it relative to its reference element. The output is
* an object with common styles and specific side styles (top/, bottom', left`, right`)
* that take into account placement`, variation`, offsets`, gpuAcceleration`,
* roundOffsets`, isFixed`, and position` properties of the input object. Additionally
* includedare side styles that depend onthe adapted side. If adaptation occurs it
* uses widthProp` or height Prop" from offsetParent' and scales  x & y positions
* depending upon whether there are variations on placement.
*/
  function mapToStyles(_ref2) {
    var _Object$assign2;

    var popper = _ref2.popper,
        popperRect = _ref2.popperRect,
        placement = _ref2.placement,
        variation = _ref2.variation,
        offsets = _ref2.offsets,
        position = _ref2.position,
        gpuAcceleration = _ref2.gpuAcceleration,
        adaptive = _ref2.adaptive,
        roundOffsets = _ref2.roundOffsets,
        isFixed = _ref2.isFixed;
    var _offsets$x = offsets.x,
        x = _offsets$x === void 0 ? 0 : _offsets$x,
        _offsets$y = offsets.y,
        y = _offsets$y === void 0 ? 0 : _offsets$y;

    var _ref3 = typeof roundOffsets === 'function' ? roundOffsets({
      x: x,
      y: y
    }) : {
      x: x,
      y: y
    };

    x = _ref3.x;
    y = _ref3.y;
    var hasX = offsets.hasOwnProperty('x');
    var hasY = offsets.hasOwnProperty('y');
    var sideX = left;
    var sideY = top;
    var win = window;

    if (adaptive) {
      var offsetParent = getOffsetParent(popper);
      var heightProp = 'clientHeight';
      var widthProp = 'clientWidth';

      if (offsetParent === getWindow(popper)) {
        offsetParent = getDocumentElement(popper);

        if (getComputedStyle$1(offsetParent).position !== 'static' && position === 'absolute') {
          heightProp = 'scrollHeight';
          widthProp = 'scrollWidth';
        }
      } // $FlowFixMe[incompatible-cast]: force type refinement, we compare offsetParent with window above, but Flow doesn't detect it


      offsetParent = offsetParent;

      if (placement === top || (placement === left || placement === right) && variation === end) {
        sideY = bottom;
        var offsetY = isFixed && offsetParent === win && win.visualViewport ? win.visualViewport.height : // $FlowFixMe[prop-missing]
        offsetParent[heightProp];
        y -= offsetY - popperRect.height;
        y *= gpuAcceleration ? 1 : -1;
      }

      if (placement === left || (placement === top || placement === bottom) && variation === end) {
        sideX = right;
        var offsetX = isFixed && offsetParent === win && win.visualViewport ? win.visualViewport.width : // $FlowFixMe[prop-missing]
        offsetParent[widthProp];
        x -= offsetX - popperRect.width;
        x *= gpuAcceleration ? 1 : -1;
      }
    }

    var commonStyles = Object.assign({
      position: position
    }, adaptive && unsetSides);

    var _ref4 = roundOffsets === true ? roundOffsetsByDPR({
      x: x,
      y: y
    }, getWindow(popper)) : {
      x: x,
      y: y
    };

    x = _ref4.x;
    y = _ref4.y;

    if (gpuAcceleration) {
      var _Object$assign;

      return Object.assign({}, commonStyles, (_Object$assign = {}, _Object$assign[sideY] = hasY ? '0' : '', _Object$assign[sideX] = hasX ? '0' : '', _Object$assign.transform = (win.devicePixelRatio || 1) <= 1 ? "translate(" + x + "px, " + y + "px)" : "translate3d(" + x + "px, " + y + "px, 0)", _Object$assign));
    }

    return Object.assign({}, commonStyles, (_Object$assign2 = {}, _Object$assign2[sideY] = hasY ? y + "px" : '', _Object$assign2[sideX] = hasX ? x + "px" : '', _Object$assign2.transform = '', _Object$assign2));
  }

/**
* @description This function `computeStyles` takes an object `_ref5` containing state
* and options properties and returns the styles for the Popper component.
* 
* @param { object } _ref5 - The `_ref5` input parameter is an object that contains
* the following properties:
* 
* 	- `state`: the current state of the component
* 	- `options`: the options object for the component.
* 
* This function takes this object as input and uses its properties to compute the
* styles and attributes for the component's popper and arrow elements.
* 
* @returns { object } The `computeStyles` function takes an object (`_ref5`) with
* properties `state` and `options`, and returns an object containing styles for the
* Popper element and the arrow element.
*/
  function computeStyles(_ref5) {
    var state = _ref5.state,
        options = _ref5.options;
    var _options$gpuAccelerat = options.gpuAcceleration,
        gpuAcceleration = _options$gpuAccelerat === void 0 ? true : _options$gpuAccelerat,
        _options$adaptive = options.adaptive,
        adaptive = _options$adaptive === void 0 ? true : _options$adaptive,
        _options$roundOffsets = options.roundOffsets,
        roundOffsets = _options$roundOffsets === void 0 ? true : _options$roundOffsets;
    var commonStyles = {
      placement: getBasePlacement(state.placement),
      variation: getVariation(state.placement),
      popper: state.elements.popper,
      popperRect: state.rects.popper,
      gpuAcceleration: gpuAcceleration,
      isFixed: state.options.strategy === 'fixed'
    };

    if (state.modifiersData.popperOffsets != null) {
      state.styles.popper = Object.assign({}, state.styles.popper, mapToStyles(Object.assign({}, commonStyles, {
        offsets: state.modifiersData.popperOffsets,
        position: state.options.strategy,
        adaptive: adaptive,
        roundOffsets: roundOffsets
      })));
    }

    if (state.modifiersData.arrow != null) {
      state.styles.arrow = Object.assign({}, state.styles.arrow, mapToStyles(Object.assign({}, commonStyles, {
        offsets: state.modifiersData.arrow,
        position: 'absolute',
        adaptive: false,
        roundOffsets: roundOffsets
      })));
    }

    state.attributes.popper = Object.assign({}, state.attributes.popper, {
      'data-popper-placement': state.placement
    });
  } // eslint-disable-next-line import/no-unused-modules


  const computeStyles$1 = {
    name: 'computeStyles',
    enabled: true,
    phase: 'beforeWrite',
    fn: computeStyles,
    data: {}
  };

  var passive = {
    passive: true
  };

/**
* @description This function takes a `state` object and an `instance` object as
* arguments and sets up event listeners for scrolling and resizing. Whenever there
* is a scroll or resize event on the window or one of the elements defined by
* `scrollParents`, the `update` method of the passed `instance` object will be called.
* 
* @param { object } _ref - The `_ref` input parameter is an object that contains the
* following properties:
* 
* 	- `state`: an object containing the state of the instance
* 	- `instance`: the current instance of the component
* 	- `options`: the options passed to the component
* 
* The `_ref` object is used to provide a way for the child component to pass its
* state and options to the parent component's methods.
* 
* @returns {  } The function `effect` takes an object with `state`, `instance`, and
* `options` properties as arguments.
*/
  function effect(_ref) {
    var state = _ref.state,
        instance = _ref.instance,
        options = _ref.options;
    var _options$scroll = options.scroll,
        scroll = _options$scroll === void 0 ? true : _options$scroll,
        _options$resize = options.resize,
        resize = _options$resize === void 0 ? true : _options$resize;
    var window = getWindow(state.elements.popper);
    var scrollParents = [].concat(state.scrollParents.reference, state.scrollParents.popper);

    if (scroll) {
      scrollParents.forEach(function (scrollParent) {
        scrollParent.addEventListener('scroll', instance.update, passive);
      });
    }

    if (resize) {
      window.addEventListener('resize', instance.update, passive);
    }

    return function () {
      if (scroll) {
        scrollParents.forEach(function (scrollParent) {
          scrollParent.removeEventListener('scroll', instance.update, passive);
        });
      }

      if (resize) {
        window.removeEventListener('resize', instance.update, passive);
      }
    };
  } // eslint-disable-next-line import/no-unused-modules


  const eventListeners = {
    name: 'eventListeners',
    enabled: true,
    phase: 'write',
/**
* @description This function does nothing as it is undefined.
* 
* @returns { any } The output returned by the function `fn()` is undefined.
*/
    fn: function fn() {},
    effect: effect,
    data: {}
  };

  var hash$1 = {
    left: 'right',
    right: 'left',
    bottom: 'top',
    top: 'bottom'
  };
/**
* @description This function takes a string representing a placement (e.g.
* 
* @param { string } placement - The `placement` input parameter is a string that
* represents the placement of an element on a web page.
* 
* @returns { string } The output returned by this function is a string that is the
* opposite of the input string based on the replacements:
* 
* 	- "left" becomes "right"
* 	- "right" becomes "left"
* 	- "bottom" becomes "top"
* 	- "top" becomes "bottom"
* 
* For example:
* 
* 	- `getOppositePlacement("left")` returns `"right"`
* 	- `getOppositePlacement("right")` returns `"left"`
* 	- `getOppositePlacement("bottom")` returns `"top"`
* 	- `getOppositePlacement("top")` returns `"bottom"`
*/
  function getOppositePlacement(placement) {
    return placement.replace(/left|right|bottom|top/g, function (matched) {
      return hash$1[matched];
    });
  }

  var hash = {
    start: 'end',
    end: 'start'
  };
/**
* @description This function takes a string representing a page layout placement
* (e.g. "start" or "end") and returns the opposite placement by replacing all
* occurrences of "start" or "end" with the corresponding hash value from an unspecified
* hash object.
* 
* @param { string } placement - The `placement` input parameter is a string that
* specifies the placement of an element (e.g., "start" or "end").
* 
* @returns { string } The output returned by this function is a string with all
* occurrences of "start" or "end" replaced with their corresponding opposite value
* (i.e. "end" becomes "start", and vice versa).
*/
  function getOppositeVariationPlacement(placement) {
    return placement.replace(/start|end/g, function (matched) {
      return hash[matched];
    });
  }

/**
* @description The `getWindowScroll` function returns an object containing the current
* scroll position of the window as viewed from a specified `node`, with properties
* for `scrollLeft` and `scrollTop`.
* 
* @param { object } node - The `node` parameter is optional and ignored inside the
* `getWindow` function.
* 
* @returns { object } The output returned by this function is an object with two
* properties: `scrollLeft` and `scrollTop`.
*/
  function getWindowScroll(node) {
    var win = getWindow(node);
    var scrollLeft = win.pageXOffset;
    var scrollTop = win.pageYOffset;
    return {
      scrollLeft: scrollLeft,
      scrollTop: scrollTop
    };
  }

/**
* @description The `getWindowScrollBarX()` function returns the x-position of the
* left scrollbar of a given HTML element taking into account both the left and top
* positions of the scrollbars.
* 
* @param { object } element - The `element` input parameter is not used inside the
* function `getWindowScrollBarX()`. The function only uses the `getBoundingClientRect()`
* and `getWindowScroll()` methods of the `element` returned by `getDocumentElement()`,
* without modifying or depending on the value of the element itself.
* 
* @returns { number } The function `getWindowScrollBarX(element)` returns the
* horizontal distance between the left edge of the viewport and the leftmost scrollbar
* element (if present) for the specified `element`. It does this by first getting
* the bounding client rect of the document element and then adding the scroll left
* position of the window.
*/
  function getWindowScrollBarX(element) {
    // If <html> has a CSS width greater than the viewport, then this will be
    // incorrect for RTL.
    // Popper 1 is broken in this case and never had a bug report so let's assume
    // it's not an issue. I don't think anyone ever specifies width on <html>
    // anyway.
    // Browsers where the left scrollbar doesn't cause an issue report `0` for
    // this (e.g. Edge 2019, IE11, Safari)
    return getBoundingClientRect(getDocumentElement(element)).left + getWindowScroll(element).scrollLeft;
  }

/**
* @description This function retrieves the viewport dimensions and scrolling position
* of an HTML element relative to the window viewport. It takes two arguments:
* 
* 	- `element`: The element whose viewport rectangle is to be obtained.
* 	- `strategy`: A string indicating the method by which to calculate the viewport
* rectangle. Options are 'auto', 'fixed', or undefined (omit to use the default value
* 'auto').
* 
* The function returns an object with four properties:
* 
* 	- `width`: The width of the viewport rectangle.
* 	- `height`: The height of the viewport rectangle.
* 	- `x`: The left coordinate of the viewport rectangle relative to the window viewport.
* 	- `y`: The top coordinate of the viewport rectangle relative to the window viewport.
* 
* It first gets the current window and document element associated with the provided
* element. Then it calculates the visual viewport dimensions (width and height) using
* `window.visualViewport`. If no visual viewport is defined (i.e., when `strategy`
* is 'auto'), it uses a heuristic to determine if the layout viewport (i.e., the
* entire contents of the document within the viewport) or the fixed viewport (the
* portion of the document that is currently visible) should be used instead.
* 
* @param {  } element - The `element` input parameter is passed to the function
* `getWindow`, which returns the window object that contains the element.
* 
* @param { string } strategy - The `strategy` parameter specifies how to calculate
* the viewport rect. Possible values are `'fixed'`, `'auto'` and ```NULL``.
* 
* @returns { object } The function `getViewportRect` returns an object with four
* properties: `width`, `height`, `x`, and `y`.
*/
  function getViewportRect(element, strategy) {
    var win = getWindow(element);
    var html = getDocumentElement(element);
    var visualViewport = win.visualViewport;
    var width = html.clientWidth;
    var height = html.clientHeight;
    var x = 0;
    var y = 0;

    if (visualViewport) {
      width = visualViewport.width;
      height = visualViewport.height;
      var layoutViewport = isLayoutViewport();

      if (layoutViewport || !layoutViewport && strategy === 'fixed') {
        x = visualViewport.offsetLeft;
        y = visualViewport.offsetTop;
      }
    }

    return {
      width: width,
      height: height,
      x: x + getWindowScrollBarX(element),
      y: y
    };
  }

  // of the `<html>` and `<body>` rect bounds if horizontally scrollable

/**
* @description This function `getDocumentRect` computes the dimensions of the rectangle
* that contains an element and its margins (horizontally and vertically), taking
* into account scrolling positions and orientation (RTL).
* 
* @param {  } element - The `element` parameter is passed to `getDocumentElement(element)`
* which returns the element's owner document (which may be null) and also body of
* that document if it exists. The rest of the function works on that document.
* 
* @returns { object } The `getDocumentRect` function returns an object with four
* properties: `width`, `height`, `x`, and `y`. These properties represent the size
* and position of the specified `element` within its document's viewport.
*/
  function getDocumentRect(element) {
    var _element$ownerDocumen;

    var html = getDocumentElement(element);
    var winScroll = getWindowScroll(element);
    var body = (_element$ownerDocumen = element.ownerDocument) == null ? void 0 : _element$ownerDocumen.body;
    var width = max(html.scrollWidth, html.clientWidth, body ? body.scrollWidth : 0, body ? body.clientWidth : 0);
    var height = max(html.scrollHeight, html.clientHeight, body ? body.scrollHeight : 0, body ? body.clientHeight : 0);
    var x = -winScroll.scrollLeft + getWindowScrollBarX(element);
    var y = -winScroll.scrollTop;

    if (getComputedStyle$1(body || html).direction === 'rtl') {
      x += max(html.clientWidth, body ? body.clientWidth : 0) - width;
    }

    return {
      width: width,
      height: height,
      x: x,
      y: y
    };
  }

/**
* @description This function checks if the given element has a scrolling container
* parent using the `getComputedStyle()` method.
* 
* @param { object } element - The `element` input parameter is passed a specific DOM
* element to determine its scroll parent according to its CSS overflow properties.
* 
* @returns { boolean } The output returned by the `isScrollParent` function is a
* boolean value indicating whether the provided element has a scrolling parent or
* not. It does this by checking the computed style of the element for certain overflow
* values (e.g. "auto", "scroll", "overlay", or "hidden") on both the X and Y axes.
* If any of these overflow values are present on either axis., the function returns
* true.
*/
  function isScrollParent(element) {
    // Firefox wants us to check `-x` and `-y` variations as well
    var _getComputedStyle = getComputedStyle$1(element),
        overflow = _getComputedStyle.overflow,
        overflowX = _getComputedStyle.overflowX,
        overflowY = _getComputedStyle.overflowY;

    return /auto|scroll|overlay|hidden/.test(overflow + overflowY + overflowX);
  }

/**
* @description This function recursively determines the scroll parent of a given
* node (the element with scrolling capabilities that contains the given node). It
* first checks if the given node is one of the top-level HTML elements (html or body)
* and returns it directly if so.
* 
* @param { object } node - The `node` parameter is passed as an argument to the
* function and it represents the DOM node for which we need to find its scroll parent
* element.
* 
* @returns {  } The `getScrollParent` function returns the scroll parent element of
* a given node. If the given node is the `html` or `body` element or an element with
* id `document`, it returns that element. Otherwise it recursively checks if the
* parent node of the given node has scroll functionality and if it does return that
* parent node as the scroll parent.
*/
  function getScrollParent(node) {
    if (['html', 'body', '#document'].indexOf(getNodeName(node)) >= 0) {
      // $FlowFixMe[incompatible-return]: assume body is always available
      return node.ownerDocument.body;
    }

    if (isHTMLElement(node) && isScrollParent(node)) {
      return node;
    }

    return getScrollParent(getParentNode(node));
  }

  /*
  given a DOM element, return the list of all scroll parents, up the list of ancesors
  until we get to the top window object. This list is what we attach scroll listeners
  to, because if any of these parent elements scroll, we'll need to re-calculate the
  reference element's position.
  */

  function listScrollParents(element, list) {
    var _element$ownerDocumen;

    if (list === void 0) {
      list = [];
    }

    var scrollParent = getScrollParent(element);
    var isBody = scrollParent === ((_element$ownerDocumen = element.ownerDocument) == null ? void 0 : _element$ownerDocumen.body);
    var win = getWindow(scrollParent);
    var target = isBody ? [win].concat(win.visualViewport || [], isScrollParent(scrollParent) ? scrollParent : []) : scrollParent;
    var updatedList = list.concat(target);
    return isBody ? updatedList : // $FlowFixMe[incompatible-call]: isBody tells us target will be an HTMLElement here
    updatedList.concat(listScrollParents(getParentNode(target)));
  }

/**
* @description This function takes a `rect` object as input and returns a new object
* with the same properties but with the values transformed from "pixel coordinates"
* (i.e. the values inside the original rect object) to "client rectangles" (i.e.
* 
* @param { object } rect - The `rect` input parameter is a plain object with properties
* `x`, `y`, `width`, and `height`, which contain the coordinates and dimensions of
* the rectangular region to be transformed.
* 
* @returns { object } This function takes a `rect` object as an argument and returns
* an object with the same properties as the original `rect` object but with different
* property names.
*/
  function rectToClientRect(rect) {
    return Object.assign({}, rect, {
      left: rect.x,
      top: rect.y,
      right: rect.x + rect.width,
      bottom: rect.y + rect.height
    });
  }

/**
* @description The function "getInnerBoundingClientRect" retrieves the bounding
* client rectangle of an element while taking into account its "clientTop", "clientLeft",
* "clientWidth", and "clientHeight".
* 
* @param { object } element - The `element` input parameter is the HTML element for
* which you want to retrieve the inner bounding client rect.
* 
* @param { string } strategy - The `strategy` input parameter specifies whether the
* bounding client rect should be computed using the "view" or "fixed" positioning strategy.
* 
* @returns { object } The `getInnerBoundingClientRect` function returns an object
* with the following properties:
* 
* 	- `top`: the top position of the element relative to its containing block
* 	- `left`: the left position of the element relative to its containing block
* 	- `bottom`: the bottom position of the element relative to its containing block
* 	- `right`: the right position of the element relative to its containing block
* 	- `width`: the width of the element
* 	- `height`: the height of the element
* 	- `x`: the x-coordinate of the top-left corner of the element
* 	- `y`: the y-coordinate of the top-left corner of the element
* 
* All positions and dimensions are relative to the element's containing block and
* take into account any applicable padding and borders.
*/
  function getInnerBoundingClientRect(element, strategy) {
    var rect = getBoundingClientRect(element, false, strategy === 'fixed');
    rect.top = rect.top + element.clientTop;
    rect.left = rect.left + element.clientLeft;
    rect.bottom = rect.top + element.clientHeight;
    rect.right = rect.left + element.clientWidth;
    rect.width = element.clientWidth;
    rect.height = element.clientHeight;
    rect.x = rect.left;
    rect.y = rect.top;
    return rect;
  }

/**
* @description This function retrieves the client rect of an element after taking
* into account its clipping parent (the ancestor element that is clipping its
* descendants), using a specified strategy.
* 
* @param { any } element - The `element` parameter is an HTML element whose bounding
* client rect is to be retrieved.
* 
* @param { any } clippingParent - The `clippingParent` parameter specifies the element
* that will be used to clip the calculation of the client rect.
* 
* @param { string } strategy - The `strategy` input parameter is used to determine
* how to compute the client rectangle.
* 
* @returns { object } The function `getClientRectFromMixedType` returns a ClientRect
* object representing the bounding client rectangle of an element (or its containing
* block), taking into account potential clipping parents and different strategies
* for calculating the rectangle.
* 
* Here's a concise description of the output:
* 
* 	- If `clippingParent` is the viewport and `strategy` is undefined or "default",
* the function returns the client rectangle of the viewport.
* 	- If `clippingParent` is an element and `strategy` is "content-box", the function
* returns the client rectangle of the element's content box (its innermost block).
* 	- If `clippingParent` is an element and `strategy` is "border-box", the function
* returns the client rectangle of the element's border box (its outermost box).
* 	- Otherwise (i.e., if `clippingParent` is not the viewport and `strategy` is not
* undefined), the function returns the client rectangle of the document element
* (which represents the entire document).
*/
  function getClientRectFromMixedType(element, clippingParent, strategy) {
    return clippingParent === viewport ? rectToClientRect(getViewportRect(element, strategy)) : isElement(clippingParent) ? getInnerBoundingClientRect(clippingParent, strategy) : rectToClientRect(getDocumentRect(getDocumentElement(element)));
  } // A "clipping parent" is an overflowable container with the characteristic of
  // clipping (or hiding) overflowing elements with a position different from
  // `initial`


/**
* @description This function getClippingParents returns an array of ancestor elements
* that contain the specified element and have a position other than "static", meaning
* they clipper their descendants.
* 
* @param { object } element - The `element` parameter is the current element being
* checked for clipping parents.
* 
* @returns { array } The `getClippingParents` function takes an element as input and
* returns an array of Elements that are parents of the element and have a clipping
* position (i.e., `position: absolute` or `position: fixed`).
*/
  function getClippingParents(element) {
    var clippingParents = listScrollParents(getParentNode(element));
    var canEscapeClipping = ['absolute', 'fixed'].indexOf(getComputedStyle$1(element).position) >= 0;
    var clipperElement = canEscapeClipping && isHTMLElement(element) ? getOffsetParent(element) : element;

    if (!isElement(clipperElement)) {
      return [];
    } // $FlowFixMe[incompatible-return]: https://github.com/facebook/flow/issues/1414


    return clippingParents.filter(function (clippingParent) {
      return isElement(clippingParent) && contains(clippingParent, clipperElement) && getNodeName(clippingParent) !== 'body';
    });
  } // Gets the maximum area that the element is visible in due to any number of
  // clipping parents


/**
* @description This function computes theclipping rect of an element by taking into
* account its boundary and ancestor boundary nodes with a strategy that considers
* their client rects.
* 
* @param {  } element - The `element` input parameter is passed as an argument to
* the internal `getClientRectFromMixedType()` function within the reduce() callback
* function and is used to retrieve the client rectangle of each clipping parent
* relative to its own coordinate system.
* 
* @param { array } boundary - The `boundary` parameter specifies a set of elements
* to include as clipping parents. It can be either an array of elements or a string
* containing a single element name.
* 
* @param {  } rootBoundary - The `rootBoundary` parameter is used to specify the
* bounds of the document element (i.e., the HTML document's root element) for
* calculating the clipping rectangle. When `rootBoundary` is not provided or is set
* to 'clippingParents', the function uses the boundaries of the main clipping parents
* to determine the clipping rectangle.
* 
* @param { object } strategy - The `strategy` input parameter determines how the
* client rectangles are computed for the clipping parents.
* 
* @returns {  } The output of this function is a object with `top`, `right`, `bottom`,
* and `left` properties representing the clipping rectangle for an element with
* respect to its parent elements using the provided strategy.
*/
  function getClippingRect(element, boundary, rootBoundary, strategy) {
    var mainClippingParents = boundary === 'clippingParents' ? getClippingParents(element) : [].concat(boundary);
    var clippingParents = [].concat(mainClippingParents, [rootBoundary]);
    var firstClippingParent = clippingParents[0];
    var clippingRect = clippingParents.reduce(function (accRect, clippingParent) {
      var rect = getClientRectFromMixedType(element, clippingParent, strategy);
      accRect.top = max(rect.top, accRect.top);
      accRect.right = min(rect.right, accRect.right);
      accRect.bottom = min(rect.bottom, accRect.bottom);
      accRect.left = max(rect.left, accRect.left);
      return accRect;
    }, getClientRectFromMixedType(element, firstClippingParent, strategy));
    clippingRect.width = clippingRect.right - clippingRect.left;
    clippingRect.height = clippingRect.bottom - clippingRect.top;
    clippingRect.x = clippingRect.left;
    clippingRect.y = clippingRect.top;
    return clippingRect;
  }

/**
* @description This function computes the offset positions of an element relative
* to a reference element based on a specified placement (top/bottom/right/left) and
* variation (start/end).
* 
* @param { object } _ref - The `_ref` input parameter is a reference object that
* contains two properties: `reference` and `element`.
* 
* @returns { object } The function `computeOffsets` returns an object with two
* properties (`x` and `y`) that represent the offset positions of the element relative
* to the reference element based on the given placement values.
*/
  function computeOffsets(_ref) {
    var reference = _ref.reference,
        element = _ref.element,
        placement = _ref.placement;
    var basePlacement = placement ? getBasePlacement(placement) : null;
    var variation = placement ? getVariation(placement) : null;
    var commonX = reference.x + reference.width / 2 - element.width / 2;
    var commonY = reference.y + reference.height / 2 - element.height / 2;
    var offsets;

    switch (basePlacement) {
      case top:
        offsets = {
          x: commonX,
          y: reference.y - element.height
        };
        break;

      case bottom:
        offsets = {
          x: commonX,
          y: reference.y + reference.height
        };
        break;

      case right:
        offsets = {
          x: reference.x + reference.width,
          y: commonY
        };
        break;

      case left:
        offsets = {
          x: reference.x - element.width,
          y: commonY
        };
        break;

      default:
        offsets = {
          x: reference.x,
          y: reference.y
        };
    }

    var mainAxis = basePlacement ? getMainAxisFromPlacement(basePlacement) : null;

    if (mainAxis != null) {
      var len = mainAxis === 'y' ? 'height' : 'width';

      switch (variation) {
        case start:
          offsets[mainAxis] = offsets[mainAxis] - (reference[len] / 2 - element[len] / 2);
          break;

        case end:
          offsets[mainAxis] = offsets[mainAxis] + (reference[len] / 2 - element[len] / 2);
          break;
      }
    }

    return offsets;
  }

/**
* @description This function detects overflowing of a Popper element beyond its
* clipping boundary based on the placement strategy and boundary specified.
* 
* @param { object } state - The `state` parameter is an object that contains the
* current state of the Popper.js instance being used.
* 
* @param { object } options - The `options` object allows for custom configuration
* of the function's behavior.
* 
* @returns { object } The `detectOverflow` function takes a `state` object and an
* optional `options` object as input. It returns an object with six properties (`top`,
* `bottom`, `left`, `right`, `vertical`, and `horizontal`) representing the overflow
* offsets for the popper element.
* 
* The function calculates the offsets by comparing the reference element's bounding
* client rect to the clipping rect (based on the specified `boundary` and `rootBoundary`)
* and the popper element's client rect. The offsets are positive when the popper
* element overflows the clipping rect and negative or 0 when it is fully contained
* within the clipping rect.
* 
* The output object has the following properties:
* 
* 	- `top`: the offset applied to the top position of the popper element (in pixels)
* 	- `bottom`: the offset applied to the bottom position of the popper element (in
* pixels)
* 	- `left`: the offset applied to the left position of the popper element (in pixels)
* 	- `right`: the offset applied to the right position of the popper element (in pixels)
* 	- `vertical`: a boolean indicating whether the overflow is vertical (true) or
* horizontal (false)
* 	- `horizontal`: a boolean indicating whether the overflow is horizontal (true)
* or vertical (false)
* 
* The function also accepts several optional parameters to customize its behavior:
* 
* 	- `placement`: the placement of the popper element (string), defaults to `state.placement`
* 	- `strategy`: the strategy for calculating offsets (string), defaults to `state.strategy`
* 	- `boundary`: the boundary element to use for clipping (string or element),
* defaults to `clippingParents`
* 	- `rootBoundary`: the root boundary element to use for clipping (string or element),
* defaults to `viewport`
* 	- `elementContext`: the context element to use when calculating offsets (string
* or element), defaults to `popper`
* 	- `altBoundary`: an alternate boundary element to use when computing overflow
* (boolean or string), defaults to `false`
* 	- `padding`: the padding object for applying additional padding to the popper
* element (an object with `top`, `right`, `bottom`, and `left` properties), defaults
* to 0
* 
* In summarizing; the `detectOverflow` function returns a popper-position overflow
* status describing if the content is on or off and if it contains what sides.
*/
  function detectOverflow(state, options) {
    if (options === void 0) {
      options = {};
    }

    var _options = options,
        _options$placement = _options.placement,
        placement = _options$placement === void 0 ? state.placement : _options$placement,
        _options$strategy = _options.strategy,
        strategy = _options$strategy === void 0 ? state.strategy : _options$strategy,
        _options$boundary = _options.boundary,
        boundary = _options$boundary === void 0 ? clippingParents : _options$boundary,
        _options$rootBoundary = _options.rootBoundary,
        rootBoundary = _options$rootBoundary === void 0 ? viewport : _options$rootBoundary,
        _options$elementConte = _options.elementContext,
        elementContext = _options$elementConte === void 0 ? popper : _options$elementConte,
        _options$altBoundary = _options.altBoundary,
        altBoundary = _options$altBoundary === void 0 ? false : _options$altBoundary,
        _options$padding = _options.padding,
        padding = _options$padding === void 0 ? 0 : _options$padding;
    var paddingObject = mergePaddingObject(typeof padding !== 'number' ? padding : expandToHashMap(padding, basePlacements));
    var altContext = elementContext === popper ? reference : popper;
    var popperRect = state.rects.popper;
    var element = state.elements[altBoundary ? altContext : elementContext];
    var clippingClientRect = getClippingRect(isElement(element) ? element : element.contextElement || getDocumentElement(state.elements.popper), boundary, rootBoundary, strategy);
    var referenceClientRect = getBoundingClientRect(state.elements.reference);
    var popperOffsets = computeOffsets({
      reference: referenceClientRect,
      element: popperRect,
      strategy: 'absolute',
      placement: placement
    });
    var popperClientRect = rectToClientRect(Object.assign({}, popperRect, popperOffsets));
    var elementClientRect = elementContext === popper ? popperClientRect : referenceClientRect; // positive = overflowing the clipping rect
    // 0 or negative = within the clipping rect

    var overflowOffsets = {
      top: clippingClientRect.top - elementClientRect.top + paddingObject.top,
      bottom: elementClientRect.bottom - clippingClientRect.bottom + paddingObject.bottom,
      left: clippingClientRect.left - elementClientRect.left + paddingObject.left,
      right: elementClientRect.right - clippingClientRect.right + paddingObject.right
    };
    var offsetData = state.modifiersData.offset; // Offsets can be applied only to the popper element

    if (elementContext === popper && offsetData) {
      var offset = offsetData[placement];
      Object.keys(overflowOffsets).forEach(function (key) {
        var multiply = [right, bottom].indexOf(key) >= 0 ? 1 : -1;
        var axis = [top, bottom].indexOf(key) >= 0 ? 'y' : 'x';
        overflowOffsets[key] += offset[axis] * multiply;
      });
    }

    return overflowOffsets;
  }

/**
* @description This function computes the best possible placement for an element
* using automatic placement (e.g., based on constraints such as boundary and padding),
* among a set of allowed placements.
* 
* @param { object } state - The `state` input parameter is not used anywhere within
* the provided code snippet of `computeAutoPlacement`. As such it has no purpose or
* effect on the functions output.
* 
* @param { object } options - The `options` object allows customizing various aspects
* of the automatic placement algorithm.
* 
* @returns { array } The function `computeAutoPlacement` takes an state object and
* options object as inputs and returns an array of possible placements for the element
* that overflows the least.
* 
* Here's a breakdown of the output:
* 
* 1/ If no valid placements are found (i.e., all possible placements have overflow),
* the function returns an empty array (`[]`).
* 2/ Otherwise (i.e., at least one valid placement is found), the function returns
* an array of possible placements sorted by the minimum amount of overflow.
* 3/ The array contains only unique placements (no duplicates) and each placement
* is represented as a string (e.g., `'start'`, `'end'`, `'top'`, etc.).
* 4/ Each element of the returned array has an associated value indicating the
* overflow amount for that specific placement. This value is determined by calculating
* the overlap between the element and the boundaries (root boundary plus padding)
* for that placement.
*/
  function computeAutoPlacement(state, options) {
    if (options === void 0) {
      options = {};
    }

    var _options = options,
        placement = _options.placement,
        boundary = _options.boundary,
        rootBoundary = _options.rootBoundary,
        padding = _options.padding,
        flipVariations = _options.flipVariations,
        _options$allowedAutoP = _options.allowedAutoPlacements,
        allowedAutoPlacements = _options$allowedAutoP === void 0 ? placements : _options$allowedAutoP;
    var variation = getVariation(placement);
    var placements$1 = variation ? flipVariations ? variationPlacements : variationPlacements.filter(function (placement) {
      return getVariation(placement) === variation;
    }) : basePlacements;
    var allowedPlacements = placements$1.filter(function (placement) {
      return allowedAutoPlacements.indexOf(placement) >= 0;
    });

    if (allowedPlacements.length === 0) {
      allowedPlacements = placements$1;
    } // $FlowFixMe[incompatible-type]: Flow seems to have problems with two array unions...


    var overflows = allowedPlacements.reduce(function (acc, placement) {
      acc[placement] = detectOverflow(state, {
        placement: placement,
        boundary: boundary,
        rootBoundary: rootBoundary,
        padding: padding
      })[getBasePlacement(placement)];
      return acc;
    }, {});
    return Object.keys(overflows).sort(function (a, b) {
      return overflows[a] - overflows[b];
    });
  }

/**
* @description The function `getExpandedFallbackPlacements` takes a `placement`
* argument and returns an array of placements that can be used as fallbacks if the
* original placement is not possible.
* 
* @param { string } placement - The `placement` input parameter specifies the starting
* placement to be expanded.
* 
* @returns { object } Based on the given function:
* 
* `getExpandedFallbackPlacements(placement)`
* 
* The output returned by this function is an array of placements. The function takes
* a placement as input and returns an array of three placements if the base placement
* is not auto.
*/
  function getExpandedFallbackPlacements(placement) {
    if (getBasePlacement(placement) === auto) {
      return [];
    }

    var oppositePlacement = getOppositePlacement(placement);
    return [getOppositeVariationPlacement(placement), oppositePlacement, getOppositeVariationPlacement(oppositePlacement)];
  }

/**
* @description This function implements the "flip" modifier for Popper.js (a JavaScript
* library for positioning elements). It determines the best placement for an element
* to be placed relative to its parent element. The function takes three arguments:
* `state`, `options`, and `name`. The function returns nothing and has several side
* effects.
* 
* Here is what the function does:
* 
* 1/ If the state has been flagged as requiring no further processing (e.g., `modal`)
* or if the option for flip variation is false (`flipVariations === false`), the
* function simply returns without doing any further processing.
* 2/ It retrieves the reference rect and popper rect from the state.
* 3/ It sets up a map to store checks that can be run to determine if a placement fits.
* 4/ It loops through the provided placements array and checks each one for feasibility
* using boundary checking and overflow detection. If a valid placement is found
* (based on main/alt axis checking and vertical positioning), it sets `firstFittingPlacement`
* to that value and breaks out of the loop.
* 5/ After finding no more feasible placements (or if there were no initial placements),
* it executes fallback checks. Fallback checks involve determining if one of a series
* of predefined "start" placements would work for the element's positioning (these
* include "top", "right", "bottom", and "left").
* 
* @param { object } _ref - The `_ref` parameter is an object that contains various
* properties related to the current placement and options. It has the following properties:
* 
* 	- `state`: The current state of the modifier.
* 	- `options`: The modifier's options Object containing mainAxis and altAxis values.
* 	- `name`: The name of the modifier.
* 
* The `_ref` parameter is used to access these properties inside the function.
* 
* @returns { string } The `flip` function takes a `state` object with various
* properties related to Popper.js modifiers and returns a boolean value indicating
* whether it has found a fitting placement for the popper.
* 
* Here's a breakdown of the output returned by the function:
* 
* 1/ If the `state.modifiersData[name]._skip` property is true (i.e., the previous
* placement attempt was skipped), the function returns `undefined`.
* 2/ Otherwise (if no previous placement attempt was skipped), the function searches
* for a fitting placement for the popper and returns `true` if it finds one or `false`
* otherwise.
* 3/ If the function returns `true`, the `state.placement` property is set to the
* first fitting placement found and the `state.reset` property is set to `true`.
* 4/ If the function returns `false`, the `state.modifiersData[name]._skip` property
* is set to `true` to indicate that no suitable placement was found and the previous
* placement will be used (or no placement will be used if there is no previous placement).
*/
  function flip(_ref) {
    var state = _ref.state,
        options = _ref.options,
        name = _ref.name;

    if (state.modifiersData[name]._skip) {
      return;
    }

    var _options$mainAxis = options.mainAxis,
        checkMainAxis = _options$mainAxis === void 0 ? true : _options$mainAxis,
        _options$altAxis = options.altAxis,
        checkAltAxis = _options$altAxis === void 0 ? true : _options$altAxis,
        specifiedFallbackPlacements = options.fallbackPlacements,
        padding = options.padding,
        boundary = options.boundary,
        rootBoundary = options.rootBoundary,
        altBoundary = options.altBoundary,
        _options$flipVariatio = options.flipVariations,
        flipVariations = _options$flipVariatio === void 0 ? true : _options$flipVariatio,
        allowedAutoPlacements = options.allowedAutoPlacements;
    var preferredPlacement = state.options.placement;
    var basePlacement = getBasePlacement(preferredPlacement);
    var isBasePlacement = basePlacement === preferredPlacement;
    var fallbackPlacements = specifiedFallbackPlacements || (isBasePlacement || !flipVariations ? [getOppositePlacement(preferredPlacement)] : getExpandedFallbackPlacements(preferredPlacement));
    var placements = [preferredPlacement].concat(fallbackPlacements).reduce(function (acc, placement) {
      return acc.concat(getBasePlacement(placement) === auto ? computeAutoPlacement(state, {
        placement: placement,
        boundary: boundary,
        rootBoundary: rootBoundary,
        padding: padding,
        flipVariations: flipVariations,
        allowedAutoPlacements: allowedAutoPlacements
      }) : placement);
    }, []);
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var checksMap = new Map();
    var makeFallbackChecks = true;
    var firstFittingPlacement = placements[0];

    for (var i = 0; i < placements.length; i++) {
      var placement = placements[i];

      var _basePlacement = getBasePlacement(placement);

      var isStartVariation = getVariation(placement) === start;
      var isVertical = [top, bottom].indexOf(_basePlacement) >= 0;
      var len = isVertical ? 'width' : 'height';
      var overflow = detectOverflow(state, {
        placement: placement,
        boundary: boundary,
        rootBoundary: rootBoundary,
        altBoundary: altBoundary,
        padding: padding
      });
      var mainVariationSide = isVertical ? isStartVariation ? right : left : isStartVariation ? bottom : top;

      if (referenceRect[len] > popperRect[len]) {
        mainVariationSide = getOppositePlacement(mainVariationSide);
      }

      var altVariationSide = getOppositePlacement(mainVariationSide);
      var checks = [];

      if (checkMainAxis) {
        checks.push(overflow[_basePlacement] <= 0);
      }

      if (checkAltAxis) {
        checks.push(overflow[mainVariationSide] <= 0, overflow[altVariationSide] <= 0);
      }

      if (checks.every(function (check) {
        return check;
      })) {
        firstFittingPlacement = placement;
        makeFallbackChecks = false;
        break;
      }

      checksMap.set(placement, checks);
    }

    if (makeFallbackChecks) {
      // `2` may be desired in some cases – research later
      var numberOfChecks = flipVariations ? 3 : 1;

/**
* @description This function iterates over an array of placements and checks whether
* each placement fits the current check by calling a function that returns true if
* the check is valid for the placement.
* 
* @param { number } _i - The `_i` input parameter is a loop counter that specifies
* the index of the current check being evaluated.
* 
* @returns { string } The output of the given function is a string "break" if there
* exists a placement that satisfies all the checks up to the current index `_i`,
* otherwise the function will continue to the next iteration.
*/
      var _loop = function _loop(_i) {
        var fittingPlacement = placements.find(function (placement) {
          var checks = checksMap.get(placement);

          if (checks) {
            return checks.slice(0, _i).every(function (check) {
              return check;
            });
          }
        });

        if (fittingPlacement) {
          firstFittingPlacement = fittingPlacement;
          return "break";
        }
      };

      for (var _i = numberOfChecks; _i > 0; _i--) {
        var _ret = _loop(_i);

        if (_ret === "break") break;
      }
    }

    if (state.placement !== firstFittingPlacement) {
      state.modifiersData[name]._skip = true;
      state.placement = firstFittingPlacement;
      state.reset = true;
    }
  } // eslint-disable-next-line import/no-unused-modules


  const flip$1 = {
    name: 'flip',
    enabled: true,
    phase: 'main',
    fn: flip,
    requiresIfExists: ['offset'],
    data: {
      _skip: false
    }
  };

/**
* @description This function calculates the side offsets (top/right/bottom/left) of
* an overflow area relative to a rectangle.
* 
* @param {  } overflow - The `overflow` input parameter provides the values of the
* vertical and horizontal offset of the rectangle's bounding box from its containing
* block's border box.
* 
* @param { number } rect - The `rect` input parameter is used to determine the size
* of the bounding rectangle for the element that has overflow.
* 
* @param { object } preventedOffsets - The `preventedOffsets` input parameter to the
* `getSideOffsets()` function is used to subtract out any overflow area that is not
* allowed to be visible due to constraints.
* 
* @returns { object } The output returned by this function is an object with four
* properties: top*, right*, bottom*, and left*., Each property represents the side
* offset (in pixels) of the element when it is overflowing.
* The offsets are calculated by taking the difference between the overflow rectangles
* dimensions and the size of the element and adding any prevented Offset that are
* specified to calculate.
*/
  function getSideOffsets(overflow, rect, preventedOffsets) {
    if (preventedOffsets === void 0) {
      preventedOffsets = {
        x: 0,
        y: 0
      };
    }

    return {
      top: overflow.top - rect.height - preventedOffsets.y,
      right: overflow.right - rect.width + preventedOffsets.x,
      bottom: overflow.bottom - rect.height + preventedOffsets.y,
      left: overflow.left - rect.width - preventedOffsets.x
    };
  }

/**
* @description The function `isAnySideFullyClipped` checks if any of the sides of a
* bounding box are fully clipped (i.e., exactly on the border of the viewport) by
* checking the values of `overflow` array.
* 
* @param { object } overflow - The `overflow` input parameter represents an object
* with four properties: `top`, `right`, `bottom`, and `left`, each containing a
* number representing the amount of clipping that occurred on that side.
* 
* @returns { boolean } The function takes an `overflow` object as input and returns
* a boolean value indicating whether any of the sides of the overflow are fully
* clipped (i.e., equal to or greater than zero).
* 
* The function checks each side of the overflow using the `some()` method and the
* `Returns` return value of `false` if all sides have negative values. If any side
* has a positive value (fully clipped), the function returns `true`.
*/
  function isAnySideFullyClipped(overflow) {
    return [top, right, bottom, left].some(function (side) {
      return overflow[side] >= 0;
    });
  }

/**
* @description This function `hide` updates the state of a Popper element by:
* 
* 1/ Detecting overflow and clipping on the reference element using `detectOverflow`.
* 2/ Updating the state with new offsets and flags indicating whether the reference
* or popper element is fully clipped or escaped.
* 3/ Setting attributes on the popper element to indicate which parts of the element
* are hidden or escaped.
* 
* @param { object } _ref - The `_ref` input parameter is a object that contains the
* current state of the popper element and the reference element. It contains properties
* like `state`, `name`, `rects`, and `modifiersData`.
* 
* @returns { object } The `hide` function takes a state object as input and modifies
* it by adding new properties to the `modifiersData` object and updating the
* `attributes` object. The output returned by the function is a new state object
* with modified `modifiersData` and `attributes` objects that contain information
* about the overflow state of the reference and popper elements.
*/
  function hide(_ref) {
    var state = _ref.state,
        name = _ref.name;
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var preventedOffsets = state.modifiersData.preventOverflow;
    var referenceOverflow = detectOverflow(state, {
      elementContext: 'reference'
    });
    var popperAltOverflow = detectOverflow(state, {
      altBoundary: true
    });
    var referenceClippingOffsets = getSideOffsets(referenceOverflow, referenceRect);
    var popperEscapeOffsets = getSideOffsets(popperAltOverflow, popperRect, preventedOffsets);
    var isReferenceHidden = isAnySideFullyClipped(referenceClippingOffsets);
    var hasPopperEscaped = isAnySideFullyClipped(popperEscapeOffsets);
    state.modifiersData[name] = {
      referenceClippingOffsets: referenceClippingOffsets,
      popperEscapeOffsets: popperEscapeOffsets,
      isReferenceHidden: isReferenceHidden,
      hasPopperEscaped: hasPopperEscaped
    };
    state.attributes.popper = Object.assign({}, state.attributes.popper, {
      'data-popper-reference-hidden': isReferenceHidden,
      'data-popper-escaped': hasPopperEscaped
    });
  } // eslint-disable-next-line import/no-unused-modules


  const hide$1 = {
    name: 'hide',
    enabled: true,
    phase: 'main',
    requiresIfExists: ['preventOverflow'],
    fn: hide
  };

/**
* @description This function calculates the horizontal (x) and vertical (y) distances
* from a placement point to a reference rectangle's edges (left or top edge),
* accounting for offset values provided as arguments.
* 
* @param { string } placement - The `placement` parameter determines the orientation
* of the element relative to its parent container. It can be one of "left", "right",
* "top", or "bottom".
* 
* @param { object } rects - The `rects` input parameter provides an object with
* `left`, `top`, `right`, and `bottom` properties that define the bounds of the
* container element.
* 
* @param { object } offset - The `offset` input parameter modifies the calculation
* of `distance` and `skidding` by providing an alternative position to use for the
* base placement. When `offset` is a function. it receives the rectangles object as
* argument and returns an object with `placement` set to the original `placement` value.
* 
* @returns { object } The output returned by the `distanceAndSkiddingToXY` function
* is an object with two properties: `x` and `y`. The values of these properties
* depend on the input `placement`, `rects`, and `offset`.
* 
* The function returns an object with the following forms:
* 
* 	- If `basePlacement` is "left" or "top", the return object will have `x` equal
* to the distance between the anchor and the current rectangle's left edge (or top
* edge), and `y` equal to the skidding value (the distance between the anchor and
* the current rectangle's center).
* 	- If `basePlacement` is "right" or "bottom", the return object will have `x` equal
* to the skidding value (the distance between the anchor and the current rectangle's
* center), and `y` equal to the distance between the anchor and the current rectangle's
* right edge (or bottom edge).
* 
* The skidding value is either the offset provided or 0 if no offset was provided.
*/
  function distanceAndSkiddingToXY(placement, rects, offset) {
    var basePlacement = getBasePlacement(placement);
    var invertDistance = [left, top].indexOf(basePlacement) >= 0 ? -1 : 1;

    var _ref = typeof offset === 'function' ? offset(Object.assign({}, rects, {
      placement: placement
    })) : offset,
        skidding = _ref[0],
        distance = _ref[1];

    skidding = skidding || 0;
    distance = (distance || 0) * invertDistance;
    return [left, right].indexOf(basePlacement) >= 0 ? {
      x: distance,
      y: skidding
    } : {
      x: skidding,
      y: distance
    };
  }

/**
* @description This function computes the offset for a Popper component's placement
* based on the given state and options. It reduces an array of placements to an
* object containing X and Y coordinates for each placement.
* 
* @param { object } _ref2 - The `_ref2` input parameter is a object that contains
* various properties such as `state`, `options`, and `name`.
* 
* @returns { object } The `offset` function takes an object (`_ref2`) with properties
* `state`, `options`, and `name`, and returns an object with the same `name` property
* and a new `modifiersData` property that contains information about the popper's
* position relative to its reference element.
* 
* More specifically:
* 
* 	- The function first retrieves the `offset` property from the `options` object
* (defaulting to `[0.0 , 0.0]` if it's not present), and converts it to an array of
* two numbers representing horizontal and vertical offset respectively.
* 	- Then it uses the `placements` array to create a reducer function that takes the
* accumulator (`acc`) and each placement value (`placement`), and returns the `XY`
* position of that placement relative to the reference element's bounding rectangle
* (`distanceAndSkiddingToXY`).
*/
  function offset(_ref2) {
    var state = _ref2.state,
        options = _ref2.options,
        name = _ref2.name;
    var _options$offset = options.offset,
        offset = _options$offset === void 0 ? [0, 0] : _options$offset;
    var data = placements.reduce(function (acc, placement) {
      acc[placement] = distanceAndSkiddingToXY(placement, state.rects, offset);
      return acc;
    }, {});
    var _data$state$placement = data[state.placement],
        x = _data$state$placement.x,
        y = _data$state$placement.y;

    if (state.modifiersData.popperOffsets != null) {
      state.modifiersData.popperOffsets.x += x;
      state.modifiersData.popperOffsets.y += y;
    }

    state.modifiersData[name] = data;
  } // eslint-disable-next-line import/no-unused-modules


  const offset$1 = {
    name: 'offset',
    enabled: true,
    phase: 'main',
    requires: ['popperOffsets'],
    fn: offset
  };

/**
* @description This function calculates the offsets required for a popper element
* to be positioned correctly near its reference element using the specified placement
* strategy and returns the offsets as an object.
* 
* @param { object } _ref - The `_ref` input parameter is a reference object passed
* to the function that contains state information about the popper and its reference
* element.
* 
* @returns { object } The output returned by the `popperOffsets` function is an
* object of offsets for the popper element.
*/
  function popperOffsets(_ref) {
    var state = _ref.state,
        name = _ref.name;
    // Offsets are the actual position the popper needs to have to be
    // properly positioned near its reference element
    // This is the most basic placement, and will be adjusted by
    // the modifiers in the next step
    state.modifiersData[name] = computeOffsets({
      reference: state.rects.reference,
      element: state.rects.popper,
      strategy: 'absolute',
      placement: state.placement
    });
  } // eslint-disable-next-line import/no-unused-modules


  const popperOffsets$1 = {
    name: 'popperOffsets',
    enabled: true,
    phase: 'read',
    fn: popperOffsets,
    data: {}
  };

/**
* @description The function `getAltAxis(axis)` returns the opposite axis from the
* given `axis`.
* 
* @param { string } axis - The `axis` input parameter determines which axis to return
* as the alternate axis.
* 
* @returns { string } The function `getAltAxis` takes an argument `axis` and returns
* a string indicating the alternative axis based on the value of `axis`.
*/
  function getAltAxis(axis) {
    return axis === 'x' ? 'y' : 'x';
  }

/**
* @description The `preventOverflow` function takes a state object and an options
* object as inputs and computes the prevented offsets of the popper based on various
* boundaries and constraints such as tethering and overflow.
* 
* @param { object } _ref - The `_ref` parameter is an object that contains the current
* state of the Popper.js instance and its methods for getting or setting popper
* positions. It includes properties such as `placement`, `elements`, `popperOffsets`,
* `rects`, `modifiersData`, etc.
* 
* @returns { object } The output returned by the `preventOverflow` function is an
* object containing the prevented offset values for both main and alt axes.
*/
  function preventOverflow(_ref) {
    var state = _ref.state,
        options = _ref.options,
        name = _ref.name;
    var _options$mainAxis = options.mainAxis,
        checkMainAxis = _options$mainAxis === void 0 ? true : _options$mainAxis,
        _options$altAxis = options.altAxis,
        checkAltAxis = _options$altAxis === void 0 ? false : _options$altAxis,
        boundary = options.boundary,
        rootBoundary = options.rootBoundary,
        altBoundary = options.altBoundary,
        padding = options.padding,
        _options$tether = options.tether,
        tether = _options$tether === void 0 ? true : _options$tether,
        _options$tetherOffset = options.tetherOffset,
        tetherOffset = _options$tetherOffset === void 0 ? 0 : _options$tetherOffset;
    var overflow = detectOverflow(state, {
      boundary: boundary,
      rootBoundary: rootBoundary,
      padding: padding,
      altBoundary: altBoundary
    });
    var basePlacement = getBasePlacement(state.placement);
    var variation = getVariation(state.placement);
    var isBasePlacement = !variation;
    var mainAxis = getMainAxisFromPlacement(basePlacement);
    var altAxis = getAltAxis(mainAxis);
    var popperOffsets = state.modifiersData.popperOffsets;
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var tetherOffsetValue = typeof tetherOffset === 'function' ? tetherOffset(Object.assign({}, state.rects, {
      placement: state.placement
    })) : tetherOffset;
    var normalizedTetherOffsetValue = typeof tetherOffsetValue === 'number' ? {
      mainAxis: tetherOffsetValue,
      altAxis: tetherOffsetValue
    } : Object.assign({
      mainAxis: 0,
      altAxis: 0
    }, tetherOffsetValue);
    var offsetModifierState = state.modifiersData.offset ? state.modifiersData.offset[state.placement] : null;
    var data = {
      x: 0,
      y: 0
    };

    if (!popperOffsets) {
      return;
    }

    if (checkMainAxis) {
      var _offsetModifierState$;

      var mainSide = mainAxis === 'y' ? top : left;
      var altSide = mainAxis === 'y' ? bottom : right;
      var len = mainAxis === 'y' ? 'height' : 'width';
      var offset = popperOffsets[mainAxis];
      var min$1 = offset + overflow[mainSide];
      var max$1 = offset - overflow[altSide];
      var additive = tether ? -popperRect[len] / 2 : 0;
      var minLen = variation === start ? referenceRect[len] : popperRect[len];
      var maxLen = variation === start ? -popperRect[len] : -referenceRect[len]; // We need to include the arrow in the calculation so the arrow doesn't go
      // outside the reference bounds

      var arrowElement = state.elements.arrow;
      var arrowRect = tether && arrowElement ? getLayoutRect(arrowElement) : {
        width: 0,
        height: 0
      };
      var arrowPaddingObject = state.modifiersData['arrow#persistent'] ? state.modifiersData['arrow#persistent'].padding : getFreshSideObject();
      var arrowPaddingMin = arrowPaddingObject[mainSide];
      var arrowPaddingMax = arrowPaddingObject[altSide]; // If the reference length is smaller than the arrow length, we don't want
      // to include its full size in the calculation. If the reference is small
      // and near the edge of a boundary, the popper can overflow even if the
      // reference is not overflowing as well (e.g. virtual elements with no
      // width or height)

      var arrowLen = within(0, referenceRect[len], arrowRect[len]);
      var minOffset = isBasePlacement ? referenceRect[len] / 2 - additive - arrowLen - arrowPaddingMin - normalizedTetherOffsetValue.mainAxis : minLen - arrowLen - arrowPaddingMin - normalizedTetherOffsetValue.mainAxis;
      var maxOffset = isBasePlacement ? -referenceRect[len] / 2 + additive + arrowLen + arrowPaddingMax + normalizedTetherOffsetValue.mainAxis : maxLen + arrowLen + arrowPaddingMax + normalizedTetherOffsetValue.mainAxis;
      var arrowOffsetParent = state.elements.arrow && getOffsetParent(state.elements.arrow);
      var clientOffset = arrowOffsetParent ? mainAxis === 'y' ? arrowOffsetParent.clientTop || 0 : arrowOffsetParent.clientLeft || 0 : 0;
      var offsetModifierValue = (_offsetModifierState$ = offsetModifierState == null ? void 0 : offsetModifierState[mainAxis]) != null ? _offsetModifierState$ : 0;
      var tetherMin = offset + minOffset - offsetModifierValue - clientOffset;
      var tetherMax = offset + maxOffset - offsetModifierValue;
      var preventedOffset = within(tether ? min(min$1, tetherMin) : min$1, offset, tether ? max(max$1, tetherMax) : max$1);
      popperOffsets[mainAxis] = preventedOffset;
      data[mainAxis] = preventedOffset - offset;
    }

    if (checkAltAxis) {
      var _offsetModifierState$2;

      var _mainSide = mainAxis === 'x' ? top : left;

      var _altSide = mainAxis === 'x' ? bottom : right;

      var _offset = popperOffsets[altAxis];

      var _len = altAxis === 'y' ? 'height' : 'width';

      var _min = _offset + overflow[_mainSide];

      var _max = _offset - overflow[_altSide];

      var isOriginSide = [top, left].indexOf(basePlacement) !== -1;

      var _offsetModifierValue = (_offsetModifierState$2 = offsetModifierState == null ? void 0 : offsetModifierState[altAxis]) != null ? _offsetModifierState$2 : 0;

      var _tetherMin = isOriginSide ? _min : _offset - referenceRect[_len] - popperRect[_len] - _offsetModifierValue + normalizedTetherOffsetValue.altAxis;

      var _tetherMax = isOriginSide ? _offset + referenceRect[_len] + popperRect[_len] - _offsetModifierValue - normalizedTetherOffsetValue.altAxis : _max;

      var _preventedOffset = tether && isOriginSide ? withinMaxClamp(_tetherMin, _offset, _tetherMax) : within(tether ? _tetherMin : _min, _offset, tether ? _tetherMax : _max);

      popperOffsets[altAxis] = _preventedOffset;
      data[altAxis] = _preventedOffset - _offset;
    }

    state.modifiersData[name] = data;
  } // eslint-disable-next-line import/no-unused-modules


  const preventOverflow$1 = {
    name: 'preventOverflow',
    enabled: true,
    phase: 'main',
    fn: preventOverflow,
    requiresIfExists: ['offset']
  };

/**
* @description This function returns the scroll positions (both horizontal and
* vertical) of an HTML element as a single object with two properties: `scrollLeft`
* and `scrollTop`.
* 
* @param { object } element - The `element` parameter is passed as an HTML Element
* object to the `getHTMLElementScroll()` function and is used to retrieve its scroll
* positions.
* 
* @returns { object } The function `getHTMLElementScroll` returns an object with two
* properties: `scrollLeft` and `scrollTop`, containing the current scroll positions
* of the element on the X-axis (horizonal) and Y-axis (vertical), respectively.
*/
  function getHTMLElementScroll(element) {
    return {
      scrollLeft: element.scrollLeft,
      scrollTop: element.scrollTop
    };
  }

/**
* @description This function returns the scroll position of a given HTML element or
* window object by first checking if the input is a window object or an HTMLElement.
* If it's a window object or not an HTMLElement it returns the window scroll.
* 
* @param { object } node - The `node` input parameter is the element or window object
* for which the scroll position is to be retrieved.
* 
* @returns { number } The output of the `getNodeScroll()` function depends on the
* type of element passed as its argument. If the argument is a window object (`window`
* property), then the function returns the scroll position of that window.
*/
  function getNodeScroll(node) {
    if (node === getWindow(node) || !isHTMLElement(node)) {
      return getWindowScroll(node);
    } else {
      return getHTMLElementScroll(node);
    }
  }

/**
* @description The function `isElementScaled` checks if an element is scaled (i.e.,
* not at its original size) by comparing the dimensions of the element's bounding
* client rect and its own offset width and height.
* 
* @param {  } element - The `element` input parameter is a reference to the DOM
* element whose scaling should be checked.
* 
* @returns { boolean } The output returned by this function is a boolean value
* indicating whether the element is scaled or not. It checks if the width and height
* of the element's bounding client rectangle are different from its offsetWidth and
* offsetHeight respectively.
*/
  function isElementScaled(element) {
    var rect = element.getBoundingClientRect();
    var scaleX = round(rect.width) / element.offsetWidth || 1;
    var scaleY = round(rect.height) / element.offsetHeight || 1;
    return scaleX !== 1 || scaleY !== 1;
  } // Returns the composite rect of an element relative to its offsetParent.
  // Composite means it takes into account transforms as well as layout.


/**
* @description This function retrieves the rectangular boundaries of an element (or
* a virtual element) relative to its offset parent or the browser viewport depending
* on whether the offset parent is fixed or not and returns an object with properties
* for the x coordinate y coordinate width and height.
* 
* @param {  } elementOrVirtualElement - The `elementOrVirtualElement` input parameter
* is the element or virtual element for which we want to get the composite rect.
* 
* @param {  } offsetParent - The `offsetParent` parameter passed to the `getCompositeRect`
* function determines which element should be used as a reference for calculating
* offsets. It can be an element itself or null. When it's an element and the parent
* element of the passed element Or Virtual element. If offset parent is non-null
* then getScrolled rect for all elements except the top most block until the target
* element gets scrollbar on them. In this case ,if none of them has a scroll bar we
* recurse till we find one. Then the last non scrolling element becomes our offset
* Parent
* else(non null).
* 
* @param { boolean } isFixed - The `isFixed` parameter determines if the offset
* parent is a fixed element.
* 
* @returns { object } The `getCompositeRect` function takes an element or a virtual
* element and returns an object with the following properties:
* 
* 	- `x`: the combined position of the element and its offset parent
* 	- `y`: the combined position of the element and its offset parent
* 	- `width`: the width of the element
* 	- `height`: the height of the element
* 
* The function calculates these values by first getting the bounding client rect of
* the element and then adjusting for the scroll position of the offset parent element
* (if any).
*/
  function getCompositeRect(elementOrVirtualElement, offsetParent, isFixed) {
    if (isFixed === void 0) {
      isFixed = false;
    }

    var isOffsetParentAnElement = isHTMLElement(offsetParent);
    var offsetParentIsScaled = isHTMLElement(offsetParent) && isElementScaled(offsetParent);
    var documentElement = getDocumentElement(offsetParent);
    var rect = getBoundingClientRect(elementOrVirtualElement, offsetParentIsScaled, isFixed);
    var scroll = {
      scrollLeft: 0,
      scrollTop: 0
    };
    var offsets = {
      x: 0,
      y: 0
    };

    if (isOffsetParentAnElement || !isOffsetParentAnElement && !isFixed) {
      if (getNodeName(offsetParent) !== 'body' || // https://github.com/popperjs/popper-core/issues/1078
      isScrollParent(documentElement)) {
        scroll = getNodeScroll(offsetParent);
      }

      if (isHTMLElement(offsetParent)) {
        offsets = getBoundingClientRect(offsetParent, true);
        offsets.x += offsetParent.clientLeft;
        offsets.y += offsetParent.clientTop;
      } else if (documentElement) {
        offsets.x = getWindowScrollBarX(documentElement);
      }
    }

    return {
      x: rect.left + scroll.scrollLeft - offsets.x,
      y: rect.top + scroll.scrollTop - offsets.y,
      width: rect.width,
      height: rect.height
    };
  }

/**
* @description This function takes a list of modifiers as an argument and returns a
* list of those modifiers sorted according to their dependencies.
* 
* @param { object } modifiers - The `modifiers` input parameter is an array of
* JavaScript objects that represent dependencies for other modifiers.
* 
* @returns { array } The output returned by this function is an array of modifiers
* ordered such that any modifier that depends on another modifier is placed after
* the modifier it depends on.
* 
* In other words. This function takes a list of modifiers and sorts them recursively
* such that the ordering of the modifiers is consistent with their dependencies.
*/
  function order(modifiers) {
    var map = new Map();
    var visited = new Set();
    var result = [];
    modifiers.forEach(function (modifier) {
      map.set(modifier.name, modifier);
    }); // On visiting object, check for its dependencies and visit them recursively

/**
* @description This function recursively sorts an array of Modifiers based on their
* dependency relationships.
* 
* @param { object } modifier - The `modifier` input parameter is the current modifier
* being processed and is used to retrieve its requirements and visit them recursively.
* 
* @returns { array } This function takes a modifier object as an argument and
* recursively sorts its requires dependencies using the `visited` set to avoid
* visiting already sorted dependencies.
*/
    function sort(modifier) {
      visited.add(modifier.name);
      var requires = [].concat(modifier.requires || [], modifier.requiresIfExists || []);
      requires.forEach(function (dep) {
        if (!visited.has(dep)) {
          var depModifier = map.get(dep);

          if (depModifier) {
            sort(depModifier);
          }
        }
      });
      result.push(modifier);
    }

    modifiers.forEach(function (modifier) {
      if (!visited.has(modifier.name)) {
        // check for visited object
        sort(modifier);
      }
    });
    return result;
  }

/**
* @description This function takes an array of JavaScript module modifiers and returns
* a new array of modifiers ordered based on their dependencies and phases.
* 
* @param { object } modifiers - The `modifiers` input parameter is an array of
* modifier objects that should be ordered based on their dependencies and phases.
* 
* @returns { array } The `orderModifiers` function takes an array of modifiers as
* input and returns an array of arrays of modifiers grouped by phase.
* 
* The output is a list of modifier groups (e.g.
*/
  function orderModifiers(modifiers) {
    // order based on dependencies
    var orderedModifiers = order(modifiers); // order based on phase

    return modifierPhases.reduce(function (acc, phase) {
      return acc.concat(orderedModifiers.filter(function (modifier) {
        return modifier.phase === phase;
      }));
    }, []);
  }

/**
* @description This function creates a debounced version of a given function.
* 
* @param {  } fn - The `fn` parameter is the function to be called when the debouncing
* promise is resolved.
* 
* @returns { Promise } This function takes a function `fn` as an argument and returns
* a new function that debounces `fn`. The debounced function returns a Promise that
* resolves to the result of `fn` after a small delay (the resolution of the underlying
* Promise). If `fn` is called again before the previous call has resolved/rejected
* the debounced function will "remember" the new call and return the previous pending
* Promise.
*/
  function debounce(fn) {
    var pending;
    return function () {
      if (!pending) {
        pending = new Promise(function (resolve) {
          Promise.resolve().then(function () {
            pending = undefined;
            resolve(fn());
          });
        });
      }

      return pending;
    };
  }

/**
* @description This function takes an array of objects and merges them by name. It
* uses `reduce` to create a new object that combines the properties of each object
* with the same name.
* 
* @param { object } modifiers - The `modifiers` parameter is an array of objects
* containing information about each modifier to be applied to a base object.
* 
* @returns { object } The output returned by the `mergeByName` function is an array
* of objects. Each object contains properties from all the input objects with the
* same name (e.g., options and data), where each property is either a merged object
* or a plain value depending on if the previous object had a value for that property.
*/
  function mergeByName(modifiers) {
    var merged = modifiers.reduce(function (merged, current) {
      var existing = merged[current.name];
      merged[current.name] = existing ? Object.assign({}, existing, current, {
        options: Object.assign({}, existing.options, current.options),
        data: Object.assign({}, existing.data, current.data)
      }) : current;
      return merged;
    }, {}); // IE11 does not support Object.values

    return Object.keys(merged).map(function (key) {
      return merged[key];
    });
  }

  var DEFAULT_OPTIONS = {
    placement: 'bottom',
    modifiers: [],
    strategy: 'absolute'
  };

/**
* @description The function `areValidElements()` takes an array of elements as input
* and returns `true` if all elements have a `getBoundingClientRect` method; otherwise
* it returns `false`.
* 
* @returns { boolean } The output returned by the given function `areValidElements`
* is a boolean value indicating whether all elements passed as arguments have a valid
* bounding client rectangle or not.
* 
* In other words), the function takes an array of elements and checks if all of them
* have a well-defined `getBoundingClientRect()` method. If any of the elements do
* not have this method or return `null` when invoked. the function returns `false`.
*/
  function areValidElements() {
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return !args.some(function (element) {
      return !(element && typeof element.getBoundingClientRect === 'function');
    });
  }

/**
* @description This is a generator function that returns a Popper instance for use
* with popper.js library.
* 
* @param { object } generatorOptions - The `generatorOptions` parameter is an object
* that allows customization of the popper generation process. It can be used to
* provide default values for options and modifiers that are commonly used across
* multiple instances of Popper.js. The options and modifiers included by default
* provide a basic set of functionality that can usually cover most use cases. Still.
* However if you want to customize Popper.js beyond what the built-in options offer
* - by altering default behavior - generating your options object using a generator
* is useful.
* 
* @returns { object } The `popperGenerator` function returns an object called
* `instance` that contains properties and methods for working with Popper.js instances.
* 
* The properties include:
* 
* 	- `state`: An object with information about the popper and reference elements.
* 	- `setOptions`: A function to set new options for the popper instance.
* 	- `forceUpdate`: A function to force an update of the popper even if nothing has
* changed.
* 	- `update`: A debounced function that performs an update of the popper instance.
* 	- `destroy`: A function to destroy the popper instance and clean up any modifiers
* or effects.
* 
* The methods include:
* 
* 	- `forceUpdate()`: forces an update of the popper even if nothing has changed.
* 	- `update()`: updates the popper instance with the current state.
* 	- `destroy()`: destroys the popper instance and cleans up any modifiers or effects.
* 
* The output of the `popperGenerator` function is the `instance` object that contains
* these properties and methods for working with Popper.js instances.
*/
  function popperGenerator(generatorOptions) {
    if (generatorOptions === void 0) {
      generatorOptions = {};
    }

    var _generatorOptions = generatorOptions,
        _generatorOptions$def = _generatorOptions.defaultModifiers,
        defaultModifiers = _generatorOptions$def === void 0 ? [] : _generatorOptions$def,
        _generatorOptions$def2 = _generatorOptions.defaultOptions,
        defaultOptions = _generatorOptions$def2 === void 0 ? DEFAULT_OPTIONS : _generatorOptions$def2;
    return function createPopper(reference, popper, options) {
      if (options === void 0) {
        options = defaultOptions;
      }

      var state = {
        placement: 'bottom',
        orderedModifiers: [],
        options: Object.assign({}, DEFAULT_OPTIONS, defaultOptions),
        modifiersData: {},
        elements: {
          reference: reference,
          popper: popper
        },
        attributes: {},
        styles: {}
      };
      var effectCleanupFns = [];
      var isDestroyed = false;
      var instance = {
        state: state,
/**
* @description This function sets the `options` object for the Popper library instance
* and updates the `state.orderedModifiers` array with enabled modifiers based on
* their dependencies and phase properties.
* 
* @param { object } setOptionsAction - The `setOptionsAction` parameter is a function
* that can be passed to the `setOptions` function to modify the `state.options`
* object. It takes the current `state.options` object as an argument and returns a
* new options object with changes applied.
* 
* @returns { object } The `setOptions` function takes an optional `setOptionsAction`
* argument that is a function returning an options object. It then combines the
* default options and the passed options objects using `Object.assign`, creates a
* new list of scroll parents based on the passed references and modifiers.
* 
* The output returned by this function is a promise of an updated Popper.js instance.
*/
        setOptions: function setOptions(setOptionsAction) {
          var options = typeof setOptionsAction === 'function' ? setOptionsAction(state.options) : setOptionsAction;
          cleanupModifierEffects();
          state.options = Object.assign({}, defaultOptions, state.options, options);
          state.scrollParents = {
            reference: isElement(reference) ? listScrollParents(reference) : reference.contextElement ? listScrollParents(reference.contextElement) : [],
            popper: listScrollParents(popper)
          }; // Orders the modifiers based on their dependencies and `phase`
          // properties

          var orderedModifiers = orderModifiers(mergeByName([].concat(defaultModifiers, state.options.modifiers))); // Strip out disabled modifiers

          state.orderedModifiers = orderedModifiers.filter(function (m) {
            return m.enabled;
          });
          runModifierEffects();
          return instance.update();
        },
        // Sync update – it will always be executed, even if not necessary. This
        // is useful for low frequency updates where sync behavior simplifies the
        // logic.
        // For high frequency updates (e.g. `resize` and `scroll` events), always
        // prefer the async Popper#update method
/**
* @description This function forceUpdate() updates the popper's position based on
* the current state of the reference and popper elements and the options passed to
* the popper instance.
* 
* @returns { object } The `forceUpdate` function takes no arguments and returns the
* updated `state` object after running through all modifiers with their respective
* functions (`fn`). It stores reference and popper rects and resets the current
* update cycle on each run. If any modifier sets `state.reset` to `true`, it aborts
* the update cycle and starts again from the beginning.
*/
        forceUpdate: function forceUpdate() {
          if (isDestroyed) {
            return;
          }

          var _state$elements = state.elements,
              reference = _state$elements.reference,
              popper = _state$elements.popper; // Don't proceed if `reference` or `popper` are not valid elements
          // anymore

          if (!areValidElements(reference, popper)) {
            return;
          } // Store the reference and popper rects to be read by modifiers


          state.rects = {
            reference: getCompositeRect(reference, getOffsetParent(popper), state.options.strategy === 'fixed'),
            popper: getLayoutRect(popper)
          }; // Modifiers have the ability to reset the current update cycle. The
          // most common use case for this is the `flip` modifier changing the
          // placement, which then needs to re-run all the modifiers, because the
          // logic was previously ran for the previous placement and is therefore
          // stale/incorrect

          state.reset = false;
          state.placement = state.options.placement; // On each update cycle, the `modifiersData` property for each modifier
          // is filled with the initial data specified by the modifier. This means
          // it doesn't persist and is fresh on each update.
          // To ensure persistent data, use `${name}#persistent`

          state.orderedModifiers.forEach(function (modifier) {
            return state.modifiersData[modifier.name] = Object.assign({}, modifier.data);
          });

          for (var index = 0; index < state.orderedModifiers.length; index++) {
            if (state.reset === true) {
              state.reset = false;
              index = -1;
              continue;
            }

            var _state$orderedModifie = state.orderedModifiers[index],
                fn = _state$orderedModifie.fn,
                _state$orderedModifie2 = _state$orderedModifie.options,
                _options = _state$orderedModifie2 === void 0 ? {} : _state$orderedModifie2,
                name = _state$orderedModifie.name;

            if (typeof fn === 'function') {
              state = fn({
                state: state,
                options: _options,
                name: name,
                instance: instance
              }) || state;
            }
          }
        },
        // Async and optimistically optimized update – it will not be executed if
        // not necessary (debounced to run at most once-per-tick)
        update: debounce(function () {
          return new Promise(function (resolve) {
            instance.forceUpdate();
            resolve(state);
          });
        }),
/**
* @description This function "destroy" will:
* 
* 	- Clean up any modifier effects.
* 	- Set the object's "isDestroyed" property to "true".
* 
* @returns {  } This function does not return anything as it is an undefined function.
*/
        destroy: function destroy() {
          cleanupModifierEffects();
          isDestroyed = true;
        }
      };

      if (!areValidElements(reference, popper)) {
        return instance;
      }

      instance.setOptions(options).then(function (state) {
        if (!isDestroyed && options.onFirstUpdate) {
          options.onFirstUpdate(state);
        }
      }); // Modifiers have the ability to execute arbitrary code before the first
      // update cycle runs. They will be executed in the same order as the update
      // cycle. This is useful when a modifier adds some persistent data that
      // other modifiers need to use, but the modifier is run after the dependent
      // one.

/**
* @description This function iterates through an array of modifiers and executes
* their corresponding effects.
* 
* @returns { any } This function takes an array of object literals representing
* modifiers and applies them to the state.
*/
      function runModifierEffects() {
        state.orderedModifiers.forEach(function (_ref) {
          var name = _ref.name,
              _ref$options = _ref.options,
              options = _ref$options === void 0 ? {} : _ref$options,
              effect = _ref.effect;

          if (typeof effect === 'function') {
            var cleanupFn = effect({
              state: state,
              name: name,
              instance: instance,
              options: options
            });

/**
* @description The `noopFn` function does nothing - it is a function that returns
* nothing and has no effect on its execution.
* 
* @returns { any } The `noopFn` function does not perform any operation or return
* anything. It is a "no-operation" function that simply exists and does nothing.
* When called (e.g., `noopFn()`), it returns undefined because it does not provide
* a return statement or produce any value.
*/
            var noopFn = function noopFn() {};

            effectCleanupFns.push(cleanupFn || noopFn);
          }
        });
      }

/**
* @description This function cleanups any effects that have been added using `effect`
* property.
* 
* @returns { any } The function `cleanupModifierEffects()` does not return any value
* explicitly. Instead it clears up the `effectCleanupFns` array by calling all the
* functions stored inside it and then resetting the array to an empty one.
*/
      function cleanupModifierEffects() {
        effectCleanupFns.forEach(function (fn) {
          return fn();
        });
        effectCleanupFns = [];
      }

      return instance;
    };
  }
  var createPopper$2 = /*#__PURE__*/popperGenerator(); // eslint-disable-next-line import/no-unused-modules

  var defaultModifiers$1 = [eventListeners, popperOffsets$1, computeStyles$1, applyStyles$1];
  var createPopper$1 = /*#__PURE__*/popperGenerator({
    defaultModifiers: defaultModifiers$1
  }); // eslint-disable-next-line import/no-unused-modules

  var defaultModifiers = [eventListeners, popperOffsets$1, computeStyles$1, applyStyles$1, offset$1, flip$1, preventOverflow$1, arrow$1, hide$1];
  var createPopper = /*#__PURE__*/popperGenerator({
    defaultModifiers: defaultModifiers
  }); // eslint-disable-next-line import/no-unused-modules

  const Popper = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
    __proto__: null,
    afterMain,
    afterRead,
    afterWrite,
    applyStyles: applyStyles$1,
    arrow: arrow$1,
    auto,
    basePlacements,
    beforeMain,
    beforeRead,
    beforeWrite,
    bottom,
    clippingParents,
    computeStyles: computeStyles$1,
    createPopper,
    createPopperBase: createPopper$2,
    createPopperLite: createPopper$1,
    detectOverflow,
    end,
    eventListeners,
    flip: flip$1,
    hide: hide$1,
    left,
    main,
    modifierPhases,
    offset: offset$1,
    placements,
    popper,
    popperGenerator,
    popperOffsets: popperOffsets$1,
    preventOverflow: preventOverflow$1,
    read,
    reference,
    right,
    start,
    top,
    variationPlacements,
    viewport,
    write
  }, Symbol.toStringTag, { value: 'Module' }));

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dropdown.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$a = 'dropdown';
  const DATA_KEY$6 = 'bs.dropdown';
  const EVENT_KEY$6 = `.${DATA_KEY$6}`;
  const DATA_API_KEY$3 = '.data-api';
  const ESCAPE_KEY$2 = 'Escape';
  const TAB_KEY$1 = 'Tab';
  const ARROW_UP_KEY$1 = 'ArrowUp';
  const ARROW_DOWN_KEY$1 = 'ArrowDown';
  const RIGHT_MOUSE_BUTTON = 2; // MouseEvent.button value for the secondary button, usually the right button

  const EVENT_HIDE$5 = `hide${EVENT_KEY$6}`;
  const EVENT_HIDDEN$5 = `hidden${EVENT_KEY$6}`;
  const EVENT_SHOW$5 = `show${EVENT_KEY$6}`;
  const EVENT_SHOWN$5 = `shown${EVENT_KEY$6}`;
  const EVENT_CLICK_DATA_API$3 = `click${EVENT_KEY$6}${DATA_API_KEY$3}`;
  const EVENT_KEYDOWN_DATA_API = `keydown${EVENT_KEY$6}${DATA_API_KEY$3}`;
  const EVENT_KEYUP_DATA_API = `keyup${EVENT_KEY$6}${DATA_API_KEY$3}`;
  const CLASS_NAME_SHOW$6 = 'show';
  const CLASS_NAME_DROPUP = 'dropup';
  const CLASS_NAME_DROPEND = 'dropend';
  const CLASS_NAME_DROPSTART = 'dropstart';
  const CLASS_NAME_DROPUP_CENTER = 'dropup-center';
  const CLASS_NAME_DROPDOWN_CENTER = 'dropdown-center';
  const SELECTOR_DATA_TOGGLE$3 = '[data-bs-toggle="dropdown"]:not(.disabled):not(:disabled)';
  const SELECTOR_DATA_TOGGLE_SHOWN = `${SELECTOR_DATA_TOGGLE$3}.${CLASS_NAME_SHOW$6}`;
  const SELECTOR_MENU = '.dropdown-menu';
  const SELECTOR_NAVBAR = '.navbar';
  const SELECTOR_NAVBAR_NAV = '.navbar-nav';
  const SELECTOR_VISIBLE_ITEMS = '.dropdown-menu .dropdown-item:not(.disabled):not(:disabled)';
  const PLACEMENT_TOP = isRTL() ? 'top-end' : 'top-start';
  const PLACEMENT_TOPEND = isRTL() ? 'top-start' : 'top-end';
  const PLACEMENT_BOTTOM = isRTL() ? 'bottom-end' : 'bottom-start';
  const PLACEMENT_BOTTOMEND = isRTL() ? 'bottom-start' : 'bottom-end';
  const PLACEMENT_RIGHT = isRTL() ? 'left-start' : 'right-start';
  const PLACEMENT_LEFT = isRTL() ? 'right-start' : 'left-start';
  const PLACEMENT_TOPCENTER = 'top';
  const PLACEMENT_BOTTOMCENTER = 'bottom';
  const Default$9 = {
    autoClose: true,
    boundary: 'clippingParents',
    display: 'dynamic',
    offset: [0, 2],
    popperConfig: null,
    reference: 'toggle'
  };
  const DefaultType$9 = {
    autoClose: '(boolean|string)',
    boundary: '(string|element)',
    display: 'string',
    offset: '(array|string|function)',
    popperConfig: '(null|object|function)',
    reference: '(string|element|object)'
  };

  /**
   * Class definition
   */

  class Dropdown extends BaseComponent {
/**
* @description This function is a constructor for a component that represents a
* dropdown menu.
* 
* @param {  } element - The `element` input parameter is the actual dropdown button
* element being initialized.
* 
* @param { object } config - The `config` input parameter is an options object that
* contains configuration for the constructor.
* 
* @returns { object } The `constructor` function takes two parameters `element` and
* `config`, and it returns nothing (i.e., `undefined`).
*/
    constructor(element, config) {
      super(element, config);
      this._popper = null;
      this._parent = this._element.parentNode; // dropdown wrapper
      // TODO: v6 revert #37011 & change markup https://getbootstrap.com/docs/5.3/forms/input-group/
      this._menu = SelectorEngine.next(this._element, SELECTOR_MENU)[0] || SelectorEngine.prev(this._element, SELECTOR_MENU)[0] || SelectorEngine.findOne(SELECTOR_MENU, this._parent);
      this._inNavbar = this._detectNavbar();
    }

    // Getters
/**
* @description This function is a static property defined on the Object prototype
* that returns the `Default` property.
* 
* @returns { string } The output returned by this function is `Default$9`.
*/
    static get Default() {
      return Default$9;
    }
/**
* @description This function returns the value of a constant named `DefaultType$9`.
* 
* @returns { string } The function `DefaultType` is static and returns a constant
* value called `DefaultType$9`.
*/
    static get DefaultType() {
      return DefaultType$9;
    }
/**
* @description This function returns the value of the static field `NAME$a`.
* 
* @returns { string } The function returns `NAME$a`, which is undefined since there
* is no variable `NAME` declared or defined.
*/
    static get NAME() {
      return NAME$a;
    }

    // Public
/**
* @description This function is a toggle function that alternates between showing
* and hiding the element.
* 
* @returns {  } The output of the `toggle()` function is the result of calling either
* `hide()` or `show()` on the object inside `this`, depending on the current state
* of the object's visibility (`_isShown()` returns `true` if shown and `false` otherwise).
*/
    toggle() {
      return this._isShown() ? this.hide() : this.show();
    }
/**
* @description The function show() performs the following actions:
* 
* 1/ Checks if the element is disabled or already shown before proceeding.
* 2/ Creates a new popper object if necessary.
* 3/ Adds empty mouseover listeners to the body's immediate children on touch-enabled
* devices.
* 4/ Sets the element's focus and attributes (aria-expanded and className) to indicate
* that it is shown.
* 5/ Adds a class to the menu and element to show them.
* 
* @returns { any } The output of this function is undefined because the function
* does not return anything.
*/
    show() {
      if (isDisabled(this._element) || this._isShown()) {
        return;
      }
      const relatedTarget = {
        relatedTarget: this._element
      };
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW$5, relatedTarget);
      if (showEvent.defaultPrevented) {
        return;
      }
      this._createPopper();

      // If this is a touch-enabled device we add extra
      // empty mouseover listeners to the body's immediate children;
      // only needed because of broken event delegation on iOS
      // https://www.quirksmode.org/blog/archives/2014/02/mouse_event_bub.html
      if ('ontouchstart' in document.documentElement && !this._parent.closest(SELECTOR_NAVBAR_NAV)) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.on(element, 'mouseover', noop);
        }
      }
      this._element.focus();
      this._element.setAttribute('aria-expanded', true);
      this._menu.classList.add(CLASS_NAME_SHOW$6);
      this._element.classList.add(CLASS_NAME_SHOW$6);
      EventHandler.trigger(this._element, EVENT_SHOWN$5, relatedTarget);
    }
/**
* @description The function `hide()` is defining the behavior of hiding an element
* when it is no longer needed or shown. It first checks if the element is disabled
* or already hidden and skips the rest of the code if so.
* 
* @returns {  } The `hide()` function returns nothing (undefined) if the popover is
* disabled or not shown.
*/
    hide() {
      if (isDisabled(this._element) || !this._isShown()) {
        return;
      }
      const relatedTarget = {
        relatedTarget: this._element
      };
      this._completeHide(relatedTarget);
    }
/**
* @description This function is the `dispose()` method of an object.
* 
* @returns {  } The output of this function is undefined.
* 
* Here's a breakdown of why:
* 
* 1/ The `dispose()` method is defined inside an instance of a class that extends
* another class.
* 2/ The `dispose()` method calls `super.dispose()`, which will return the result
* of the `dispose()` method of the parent class (i.e., the `Disposable` class).
* 3/ The `Disposable` class does not have an implementation for its `dispose()` method.
* 4/ Since there is no implementation for the `dispose()` method of the parent class
* (`Disposable`), the result of calling `super.dispose()` will be `undefined`.
* 5/ Therefore the output of the entire `dispose()` method will be `undefined`.
*/
    dispose() {
      if (this._popper) {
        this._popper.destroy();
      }
      super.dispose();
    }
/**
* @description The `update` function checks if the component is inside a navbar and
* updates the Popper instance.
* 
* @returns { any } The `update()` function returns nothing (i.e., `undefined`) as
* it does not have any explicit return statement.
*/
    update() {
      this._inNavbar = this._detectNavbar();
      if (this._popper) {
        this._popper.update();
      }
    }

    // Private
/**
* @description This function `completeHide` does the following:
* 
* 1/ Removes the "show" class from the menu and element.
* 2/ Destroys the popper object if it exists.
* 3/ Removes the "aria-expanded" attribute from the element.
* 4/ Removes a data attribute from the menu.
* 5/ Triggers an `hidden` event on the element.
* 
* @param {  } relatedTarget - The `relatedTarget` input parameter is the element
* that triggered the hiding of the menu.
* 
* @returns { any } This function `_completeHide` returns nothing or void as it does
* not have a return statement.
*/
    _completeHide(relatedTarget) {
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE$5, relatedTarget);
      if (hideEvent.defaultPrevented) {
        return;
      }

      // If this is a touch-enabled device we remove the extra
      // empty mouseover listeners we added for iOS support
      if ('ontouchstart' in document.documentElement) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.off(element, 'mouseover', noop);
        }
      }
      if (this._popper) {
        this._popper.destroy();
      }
      this._menu.classList.remove(CLASS_NAME_SHOW$6);
      this._element.classList.remove(CLASS_NAME_SHOW$6);
      this._element.setAttribute('aria-expanded', 'false');
      Manipulator.removeDataAttribute(this._menu, 'popper');
      EventHandler.trigger(this._element, EVENT_HIDDEN$5, relatedTarget);
    }
/**
* @description This function is a decorator that validate the configuration object
* passed to it. It checks if the "reference" option is an object and doesn't have a
* "getBoundingClientRect" method.
* 
* @param { object } config - The `config` input parameter is the configuration object
* that is being passed to the Popper component.
* 
* @returns { object } The output returned by this function is the original `config`
* object passed as an argument but with some modifications:
* 
* 1/ If `config.reference` is an object and doesn't have a `getBoundingClientRect`
* method defined within it (meaning it is not a real DOM element), then the function
* throws an error.
* 2/ If the object type checks pass successfully and no errors occur during this
* step-up of checks), then the original `config` object is simply returned unchanged
* at the end.
*/
    _getConfig(config) {
      config = super._getConfig(config);
      if (typeof config.reference === 'object' && !isElement$1(config.reference) && typeof config.reference.getBoundingClientRect !== 'function') {
        // Popper virtual elements require a getBoundingClientRect method
        throw new TypeError(`${NAME$a.toUpperCase()}: Option "reference" provided type "object" without a required "getBoundingClientRect" method.`);
      }
      return config;
    }
/**
* @description This function creates a Popper instance to display the dropdown menu
* next to its reference element (the parent or specified element).
* 
* @returns { object } The `createPopper()` function takes an element and an object
* of configuration settings for Popper.js as inputs and creates a new instance of
* Popper.js using those configurations.
*/
    _createPopper() {
      if (typeof Popper === 'undefined') {
        throw new TypeError('Bootstrap\'s dropdowns require Popper (https://popper.js.org)');
      }
      let referenceElement = this._element;
      if (this._config.reference === 'parent') {
        referenceElement = this._parent;
      } else if (isElement$1(this._config.reference)) {
        referenceElement = getElement(this._config.reference);
      } else if (typeof this._config.reference === 'object') {
        referenceElement = this._config.reference;
      }
      const popperConfig = this._getPopperConfig();
      this._popper = createPopper(referenceElement, this._menu, popperConfig);
    }
/**
* @description This function checks if the menu is currently shown (i.e., visible
* and not hidden) by checking if its class list contains a specific class name (in
* this case `CLASS_NAME_SHOW$6`).
* 
* @returns { boolean } This function returns `true` if the menu has the class
* `CLASS_NAME_SHOW$6`, and `false` otherwise.
*/
    _isShown() {
      return this._menu.classList.contains(CLASS_NAME_SHOW$6);
    }
/**
* @description This function retrieves the placement of a dropdown menu based on the
* CSS classes of its parent element.
* 
* @returns { string } This function takes no arguments and returns a string representing
* the placement of a dropdown menu relative to its parent dropdown element.
*/
    _getPlacement() {
      const parentDropdown = this._parent;
      if (parentDropdown.classList.contains(CLASS_NAME_DROPEND)) {
        return PLACEMENT_RIGHT;
      }
      if (parentDropdown.classList.contains(CLASS_NAME_DROPSTART)) {
        return PLACEMENT_LEFT;
      }
      if (parentDropdown.classList.contains(CLASS_NAME_DROPUP_CENTER)) {
        return PLACEMENT_TOPCENTER;
      }
      if (parentDropdown.classList.contains(CLASS_NAME_DROPDOWN_CENTER)) {
        return PLACEMENT_BOTTOMCENTER;
      }

      // We need to trim the value because custom properties can also include spaces
      const isEnd = getComputedStyle(this._menu).getPropertyValue('--bs-position').trim() === 'end';
      if (parentDropdown.classList.contains(CLASS_NAME_DROPUP)) {
        return isEnd ? PLACEMENT_TOPEND : PLACEMENT_TOP;
      }
      return isEnd ? PLACEMENT_BOTTOMEND : PLACEMENT_BOTTOM;
    }
/**
* @description This function detectNavbar checks if the element has a navbar ancestor.
* 
* @returns { boolean } The function `_detectNavbar()` returns a boolean value
* indicating whether the current element (represented by `this._element`) is contained
* within a navbar element (using the selector `SELECTOR_NAVBAR`).
*/
    _detectNavbar() {
      return this._element.closest(SELECTOR_NAVBAR) !== null;
    }
/**
* @description This function `_getOffset` returns the offset of a popper element
* based on the configuration object's `offset` property.
* 
* @returns { array } The function `_getOffset` returns an array of numbers.
*/
    _getOffset() {
      const {
        offset
      } = this._config;
      if (typeof offset === 'string') {
        return offset.split(',').map(value => Number.parseInt(value, 10));
      }
      if (typeof offset === 'function') {
        return popperData => offset(popperData, this._element);
      }
      return offset;
    }
/**
* @description This function prepares the configuration for a Popper.js instance
* that will be used to position the dropdown menu next to the navbar item.
* 
* @returns { object } The output returned by this function is an object that contains
* the popper configuration. It consists of the default BS Popper config and the
* modified config from the `execute()` function.
* 
* The default BS Popper config includes placement and modifiers (e.g., preventOverflow
* and offset), while the modified config is based on whether the Dropdown is inside
* a navbar or has a static display. If either of those conditions are true;
* Manipulator.setDataAttribute() method sets "popper" attribute to "static".
* 
* The output's structure is similar to this: {...defaultBsPopperConfig., ...execuete([])}.
*/
    _getPopperConfig() {
      const defaultBsPopperConfig = {
        placement: this._getPlacement(),
        modifiers: [{
          name: 'preventOverflow',
          options: {
            boundary: this._config.boundary
          }
        }, {
          name: 'offset',
          options: {
            offset: this._getOffset()
          }
        }]
      };

      // Disable Popper if we have a static display or Dropdown is in Navbar
      if (this._inNavbar || this._config.display === 'static') {
        Manipulator.setDataAttribute(this._menu, 'popper', 'static'); // TODO: v6 remove
        defaultBsPopperConfig.modifiers = [{
          name: 'applyStyles',
          enabled: false
        }];
      }
      return {
        ...defaultBsPopperConfig,
        ...execute(this._config.popperConfig, [defaultBsPopperConfig])
      };
    }
/**
* @description This function selects the next active menu item based on the current
* key press (arrow up or arrow down) and the target element. If the target element
* is not found among the visible items or there are no more active items left to
* cycle through.
* 
* @returns { object } The function `_selectMenuItem` returns no output; instead it
* focuses the next active element when arrow up or down keys are pressed and has a
* specific target that doesn't exist among the visible menu items using `SelectorEngine`.
*/
    _selectMenuItem({
      key,
      target
    }) {
      const items = SelectorEngine.find(SELECTOR_VISIBLE_ITEMS, this._menu).filter(element => isVisible(element));
      if (!items.length) {
        return;
      }

      // if target isn't included in items (e.g. when expanding the dropdown)
      // allow cycling to get the last item in case key equals ARROW_UP_KEY
      getNextActiveElement(items, target, key === ARROW_DOWN_KEY$1, !items.includes(target)).focus();
    }

    // Static
/**
* @description This function is a jQuery plugin called `jQueryInterface` that provides
* an instance of the `Dropdown` class to each selected element.
* 
* @param { object } config - The `config` parameter is an options object that specifies
* configuration for the Dropdown instance being created or modified. It can contain
* method names as keys to be called on the instance.
* 
* @returns { any } The output returned by this function is `this`.
*/
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Dropdown.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
/**
* @description This function handles clicking and tabbing events on a page with
* dropdown menus to close any open dropdowns that are not the target of the event.
* 
* @param {  } event - The `event` input parameter is used to determine when to close
* an open dropdown menu.
* 
* @returns {  } The output returned by this function is null or undefined because
* the function does not have a return statement.
*/
    static clearMenus(event) {
      if (event.button === RIGHT_MOUSE_BUTTON || event.type === 'keyup' && event.key !== TAB_KEY$1) {
        return;
      }
      const openToggles = SelectorEngine.find(SELECTOR_DATA_TOGGLE_SHOWN);
      for (const toggle of openToggles) {
        const context = Dropdown.getInstance(toggle);
        if (!context || context._config.autoClose === false) {
          continue;
        }
        const composedPath = event.composedPath();
        const isMenuTarget = composedPath.includes(context._menu);
        if (composedPath.includes(context._element) || context._config.autoClose === 'inside' && !isMenuTarget || context._config.autoClose === 'outside' && isMenuTarget) {
          continue;
        }

        // Tab navigation through the dropdown menu or events from contained inputs shouldn't close the menu
        if (context._menu.contains(event.target) && (event.type === 'keyup' && event.key === TAB_KEY$1 || /input|select|option|textarea|form/i.test(event.target.tagName))) {
          continue;
        }
        const relatedTarget = {
          relatedTarget: context._element
        };
        if (event.type === 'click') {
          relatedTarget.clickEvent = event;
        }
        context._completeHide(relatedTarget);
      }
    }
/**
* @description This function is a keydown handler for a custom dropdown component
* that checks if the input/textarea and if the key pressed is not escape or up/down
* arrow key.
* 
* @param { object } event - The `event` input parameter is used to handle keydown
* events on an element with the class `data-api`.
* 
* @returns { any } This function is an event handler for keyboard keydown events on
* elements with a specific class (not specified here). It determines if the key press
* is a dropdown command or not. If it's not an arrow key (up or down) or the escape
* key，the function prevents the default behavior and does nothing. If the event
* target is an input/textarea and the key pressed isn't an arrow or escape，the
* function does nothing as well.
* 
* Otherwise，it finds a nearby data-toggle button using a selector，creates or retrieves
* an instance of the Dropdown class，shows or hides the dropdown based on whether it
* is already visible (based on an underscore property), and sets focus back to the
* toggle button.
*/
    static dataApiKeydownHandler(event) {
      // If not an UP | DOWN | ESCAPE key => not a dropdown command
      // If input/textarea && if key is other than ESCAPE => not a dropdown command

      const isInput = /input|textarea/i.test(event.target.tagName);
      const isEscapeEvent = event.key === ESCAPE_KEY$2;
      const isUpOrDownEvent = [ARROW_UP_KEY$1, ARROW_DOWN_KEY$1].includes(event.key);
      if (!isUpOrDownEvent && !isEscapeEvent) {
        return;
      }
      if (isInput && !isEscapeEvent) {
        return;
      }
      event.preventDefault();

      // TODO: v6 revert #37011 & change markup https://getbootstrap.com/docs/5.3/forms/input-group/
      const getToggleButton = this.matches(SELECTOR_DATA_TOGGLE$3) ? this : SelectorEngine.prev(this, SELECTOR_DATA_TOGGLE$3)[0] || SelectorEngine.next(this, SELECTOR_DATA_TOGGLE$3)[0] || SelectorEngine.findOne(SELECTOR_DATA_TOGGLE$3, event.delegateTarget.parentNode);
      const instance = Dropdown.getOrCreateInstance(getToggleButton);
      if (isUpOrDownEvent) {
        event.stopPropagation();
        instance.show();
        instance._selectMenuItem(event);
        return;
      }
      if (instance._isShown()) {
        // else is escape and we check if it is shown
        event.stopPropagation();
        instance.hide();
        getToggleButton.focus();
      }
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_KEYDOWN_DATA_API, SELECTOR_DATA_TOGGLE$3, Dropdown.dataApiKeydownHandler);
  EventHandler.on(document, EVENT_KEYDOWN_DATA_API, SELECTOR_MENU, Dropdown.dataApiKeydownHandler);
  EventHandler.on(document, EVENT_CLICK_DATA_API$3, Dropdown.clearMenus);
  EventHandler.on(document, EVENT_KEYUP_DATA_API, Dropdown.clearMenus);
  EventHandler.on(document, EVENT_CLICK_DATA_API$3, SELECTOR_DATA_TOGGLE$3, function (event) {
    event.preventDefault();
    Dropdown.getOrCreateInstance(this).toggle();
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Dropdown);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/backdrop.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$9 = 'backdrop';
  const CLASS_NAME_FADE$4 = 'fade';
  const CLASS_NAME_SHOW$5 = 'show';
  const EVENT_MOUSEDOWN = `mousedown.bs.${NAME$9}`;
  const Default$8 = {
    className: 'modal-backdrop',
    clickCallback: null,
    isAnimated: false,
    isVisible: true,
    // if false, we use the backdrop helper without adding any element to the dom
    rootElement: 'body' // give the choice to place backdrop under different elements
  };

  const DefaultType$8 = {
    className: 'string',
    clickCallback: '(function|null)',
    isAnimated: 'boolean',
    isVisible: 'boolean',
    rootElement: '(element|string)'
  };

  /**
   * Class definition
   */

  class Backdrop extends Config {
/**
* @description This function is a constructor for an object that initializes the
* object's properties and prepares it for use.
* 
* @param { object } config - The `config` input parameter is used to pass configuration
* options to the constructor.
* 
* @returns { any } This is a JavaScript constructor function for an object.
*/
    constructor(config) {
      super();
      this._config = this._getConfig(config);
      this._isAppended = false;
      this._element = null;
    }

    // Getters
/**
* @description This function is a static method that returns the `Default` object.
* 
* @returns { string } The output returned by the function is `Default$8`.
*/
    static get Default() {
      return Default$8;
    }
/**
* @description This function is a getter method for the `DefaultType` property of
* the class that defines it.
* 
* @returns { string } The function `get DefaultType()` returns the value `DefaultType$8`.
*/
    static get DefaultType() {
      return DefaultType$8;
    }
/**
* @description The function is a getter for a property named `NAME`.
* 
* @returns { string } The output returned by this function is "NAME$9".
*/
    static get NAME() {
      return NAME$9;
    }

    // Public
/**
* @description This function shows an element by adding a class name and emulating
* an animation to give the appearance of a slide-in effect.
* 
* @param {  } callback - The `callback` input parameter is a function that is executed
* when the show animation has completed.
* 
* @returns { any } The `show` function returns nothing (i.e., it is void) and performs
* the following actions:
* 
* 1/ If the widget is not visible (i.e., `this._config.isVisible` is false), it
* executes the provided `callback` function immediately.
* 2/ It appends the widget's element to its parent container.
* 3/ It adds a CSS class to the element to indicate that the widget is shown.
* 4/ If animation is enabled (i.e., `this._config.isAnimated` is true), it reflows
* the element to trigger the animation.
* 5/ It emulates an animation by calling the provided `callback` function after a
* brief delay (represented by the arrow function).
* 
* In concise terms: the `show` function displays the widget's element by appending
* it to its parent container and animating it into visibility if animation is enabled.
*/
    show(callback) {
      if (!this._config.isVisible) {
        execute(callback);
        return;
      }
      this._append();
      const element = this._getElement();
      if (this._config.isAnimated) {
        reflow(element);
      }
      element.classList.add(CLASS_NAME_SHOW$5);
      this._emulateAnimation(() => {
        execute(callback);
      });
    }
/**
* @description This function is a callback function for an event and its purpose is
* to hide an element by removing a class from it. The function first checks if the
* element is already not visible (based on the _config object's isVisible property),
* and if so it immediately executes the callback function.
* 
* @param {  } callback - The `callback` parameter is a function that will be called
* after the element has been hidden (i.e., after the `dispose()` method has been called).
* 
* @returns { any } The function takes a `callback` function as an argument and returns
* its output after executing it. However (as described by the surrounding code), the
* function only executes the `callback` function if the component is currently invisible.
*/
    hide(callback) {
      if (!this._config.isVisible) {
        execute(callback);
        return;
      }
      this._getElement().classList.remove(CLASS_NAME_SHOW$5);
      this._emulateAnimation(() => {
        this.dispose();
        execute(callback);
      });
    }
/**
* @description This function disposables a element by removing it and unregistering
* an event handler.
* 
* @returns {  } The function `dispose` takes no arguments and returns nothing (undefined).
*/
    dispose() {
      if (!this._isAppended) {
        return;
      }
      EventHandler.off(this._element, EVENT_MOUSEDOWN);
      this._element.remove();
      this._isAppended = false;
    }

    // Private
/**
* @description This function creates and returns the underlying element of amodal component.
* 
* @returns {  } The function `_getElement()` creates and returns a `div` element
* using `document.createElement()`. If the function is called for the first time and
* no element has been created before (i.e., `this._element === undefined`), it creates
* an animated fade-in effect by adding a CSS class name to the div.
*/
    _getElement() {
      if (!this._element) {
        const backdrop = document.createElement('div');
        backdrop.className = this._config.className;
        if (this._config.isAnimated) {
          backdrop.classList.add(CLASS_NAME_FADE$4);
        }
        this._element = backdrop;
      }
      return this._element;
    }
/**
* @description This function sets the `rootElement` property of the passed `config`
* object to a freshly created ` Element` instance each time it's called.
* 
* @param { object } config - The `config` input parameter is a configuration object
* that is passed to the function and contains information such as the root element.
* 
* @returns { object } The output of the function is a new configuration object
* `config` with the `rootElement` property set to a freshly obtained `Element`
* instance using `getElement(default)` on each invocation. In other words.
*/
    _configAfterMerge(config) {
      // use getElement() with the default "body" to get a fresh Element on each instantiation
      config.rootElement = getElement(config.rootElement);
      return config;
    }
/**
* @description This function appends an element to the rootElement of a DOM structure
* and registers an event listener for mouse down events on that element.
* 
* @returns { any } The `append` function returns nothing (void) and does not have a
* specified output type.
*/
    _append() {
      if (this._isAppended) {
        return;
      }
      const element = this._getElement();
      this._config.rootElement.append(element);
      EventHandler.on(element, EVENT_MOUSEDOWN, () => {
        execute(this._config.clickCallback);
      });
      this._isAppended = true;
    }
/**
* @description This function emulates an animation by calling a callback function
* after a transition (either a change to a new element or a change to a new
* configuration) if the animation is configured as animated.
* 
* @param {  } callback - The `callback` input parameter is a function that will be
* executed after the transition has completed.
* 
* @returns { any } The output of `undefined` is returned by the `emptyFunction()`
* that is called inside the `_emulateAnimation()` function.
*/
    _emulateAnimation(callback) {
      executeAfterTransition(callback, this._getElement(), this._config.isAnimated);
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/focustrap.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$8 = 'focustrap';
  const DATA_KEY$5 = 'bs.focustrap';
  const EVENT_KEY$5 = `.${DATA_KEY$5}`;
  const EVENT_FOCUSIN$2 = `focusin${EVENT_KEY$5}`;
  const EVENT_KEYDOWN_TAB = `keydown.tab${EVENT_KEY$5}`;
  const TAB_KEY = 'Tab';
  const TAB_NAV_FORWARD = 'forward';
  const TAB_NAV_BACKWARD = 'backward';
  const Default$7 = {
    autofocus: true,
    trapElement: null // The element to trap focus inside of
  };

  const DefaultType$7 = {
    autofocus: 'boolean',
    trapElement: 'element'
  };

  /**
   * Class definition
   */

  class FocusTrap extends Config {
/**
* @description This function is a constructor for an object that sets up the object's
* properties and initializes its state based on the provided `config` object.
* 
* @param { object } config - The `config` input parameter is used to pass configuration
* options to the constructor of the object.
* 
* @returns { object } The function returns `undefined`.
*/
    constructor(config) {
      super();
      this._config = this._getConfig(config);
      this._isActive = false;
      this._lastTabNavDirection = null;
    }

    // Getters
/**
* @description This function is a getter for the `Default` static property of an object.
* 
* @returns { string } The output returned by the function is `Default$7`.
*/
    static get Default() {
      return Default$7;
    }
/**
* @description This function returns a constant value called `DefaultType$7`.
* 
* @returns { string } The output returned by this function is `DefaultType$7`.
*/
    static get DefaultType() {
      return DefaultType$7;
    }
/**
* @description This is a JavaScript function that returns the value of the `NAME` constant.
* 
* @returns { string } The function returns the string "undefined". The function is
* undefined itself (as denoted by the `static` keyword), and it does not have a
* `NAME` property to return.
*/
    static get NAME() {
      return NAME$8;
    }

    // Public
/**
* @description This function activates the modal and sets up event listeners for
* handling focus and key presses.
* 
* @returns {  } The `activate()` function returns nothing (void), as it is a
* void-returning function.
* 
* The function performs several actions:
* 
* 1/ Checks if the component is already active and returns immediately if so.
* 2/ Sets focus on the configured element if `autofocus` is set to true.
* 3/ Unregisters an event listener for `EVENT_KEY` (guard against infinite focus loop).
* 4/ Registers new event listeners for `EVENT_FOCUSIN` and `EVENT_KEYDOWN_TAB`.
* 5/ Sets the component's `isActive` flag to true.
*/
    activate() {
      if (this._isActive) {
        return;
      }
      if (this._config.autofocus) {
        this._config.trapElement.focus();
      }
      EventHandler.off(document, EVENT_KEY$5); // guard against infinite focus loop
      EventHandler.on(document, EVENT_FOCUSIN$2, event => this._handleFocusin(event));
      EventHandler.on(document, EVENT_KEYDOWN_TAB, event => this._handleKeydown(event));
      this._isActive = true;
    }
/**
* @description This function is a `deactivate()` method that does the following:
* 
* 1/ Checks if the component is already not active (i.e., `_isActive` is false).
* 2/ Sets `_isActive` to false.
* 3/ Removes an event listener from `document` using `EventHandler.off()` with the
* event type specified by `EVENT_KEY$5`.
* 
* @returns {  } The output of the `deactivate()` function is void.
* 
* The function first checks if the component is not already deactivated (`this._isActive
* === false`). If that's the case there is nothing to do and the function returns.
* 
* If the component is active (i.e., `_isActive === true`) the function sets
* `this._isActive` to `false`, removes any listeners on the `EVENT_KEY$5` event from
* the document using `EventHandler.off(document ...
*/
    deactivate() {
      if (!this._isActive) {
        return;
      }
      this._isActive = false;
      EventHandler.off(document, EVENT_KEY$5);
    }

    // Private
/**
* @description This function is an event handler for the `focusin` event and handles
* tab navigation between focusable elements.
* 
* @param { object } event - The `event` input parameter is not used within the
* provided code snippet.
* 
* @returns { any } This function is a JavaScript method that handles focus changes
* within a specific element (referred to as `trapElement`). The output returned by
* this function is not explicitly stated but can be inferred based on its functionality.
* Here's a concise description:
* 
* The function determines which child elements of `trapElement` should receive focus
* based on the tab navigation direction (either forward or backward) and the current
* focused element. If there are no focusable children elements within `trapElement`,
* it sets the focus on the element itself. Otherwise(i), if the previous tab navigation
* direction was backwards (TAB_NAV_BACKWARD), the function sets the focus on the
* last focusable child element of `trapElement`.
*/
    _handleFocusin(event) {
      const {
        trapElement
      } = this._config;
      if (event.target === document || event.target === trapElement || trapElement.contains(event.target)) {
        return;
      }
      const elements = SelectorEngine.focusableChildren(trapElement);
      if (elements.length === 0) {
        trapElement.focus();
      } else if (this._lastTabNavDirection === TAB_NAV_BACKWARD) {
        elements[elements.length - 1].focus();
      } else {
        elements[0].focus();
      }
    }
/**
* @description This function listens for the `keydown` event on a DOM element and
* handles the `TAB_KEY` keycode.
* 
* @param {  } event - The `event` parameter is an object containing information about
* the keypress event that triggered the function.
* 
* @returns { object } The output returned by this function is undefined.
*/
    _handleKeydown(event) {
      if (event.key !== TAB_KEY) {
        return;
      }
      this._lastTabNavDirection = event.shiftKey ? TAB_NAV_BACKWARD : TAB_NAV_FORWARD;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/scrollBar.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const SELECTOR_FIXED_CONTENT = '.fixed-top, .fixed-bottom, .is-fixed, .sticky-top';
  const SELECTOR_STICKY_CONTENT = '.sticky-top';
  const PROPERTY_PADDING = 'padding-right';
  const PROPERTY_MARGIN = 'margin-right';

  /**
   * Class definition
   */

  class ScrollBarHelper {
/**
* @description This function sets the `this._element` property of the constructor
* to the `document.body` element.
* 
* @returns { object } The output of this function is `null`.
* 
* The constructor function attempts to access `document.body` before it has been
* defined or initialized.
*/
    constructor() {
      this._element = document.body;
    }

    // Public
/**
* @description The function returns the width of the viewport (the browser window),
* minus the width of the document element (the part of the page that contains the content).
* 
* @returns { number } The function gets the width of the window's viewport and returns
* the difference between the innerWidth and the clientWidth of the document element.
* 
* The output is the absolute value of the difference between the two measurements (
* InnerWidth and ClientWidth). Therefore the output can be either positive or negative
* values.
*/
    getWidth() {
      // https://developer.mozilla.org/en-US/docs/Web/API/Window/innerWidth#usage_notes
      const documentWidth = document.documentElement.clientWidth;
      return Math.abs(window.innerWidth - documentWidth);
    }
/**
* @description The `hide()` function adjusts the padding and margin of an element
* to hide a scrollbar that is too wide for the content.
* 
* @returns {  } Based on the code provided:
* 
* The output of `hide()` function is adding padding and margin properties to the
* element's style to hide the scrollbar and keep the content sticky.
*/
    hide() {
      const width = this.getWidth();
      this._disableOverFlow();
      // give padding to element to balance the hidden scrollbar width
      this._setElementAttributes(this._element, PROPERTY_PADDING, calculatedValue => calculatedValue + width);
      // trick: We adjust positive paddingRight and negative marginRight to sticky-top elements to keep showing fullwidth
      this._setElementAttributes(SELECTOR_FIXED_CONTENT, PROPERTY_PADDING, calculatedValue => calculatedValue + width);
      this._setElementAttributes(SELECTOR_STICKY_CONTENT, PROPERTY_MARGIN, calculatedValue => calculatedValue - width);
    }
/**
* @description This function reset the attribute of elements to their default value.
* 
* @returns { any } The function `reset()` reset attribute properties of some elements
* according to some conditions described inside the code snippet above.
* Here's what you need to know about it:
* 1/ it sets the `overflow` attribute to whatever `undefined` means for an element
* ( presumably "none" or null) because `this._resetElementAttributes` resets this attributes
* 2/ it set padding property of some elements whose selector( a string ) are provided
* by ' PROPERTY_PADDING', which suggests all their padding properties might be
* affected equally by whatever value the same function return or set. For example
* this line would change (all of these properties? to some "same value").
* 3/ same idea goes for Lines 3 and 4 where sticky/fixed content properties are
* updated  with the seeming goal of uniformly removing all margins off those contents
* (perhaps resetting) with a specific property.
*/
    reset() {
      this._resetElementAttributes(this._element, 'overflow');
      this._resetElementAttributes(this._element, PROPERTY_PADDING);
      this._resetElementAttributes(SELECTOR_FIXED_CONTENT, PROPERTY_PADDING);
      this._resetElementAttributes(SELECTOR_STICKY_CONTENT, PROPERTY_MARGIN);
    }
/**
* @description This function checks if the width of the object is greater than 0.
* 
* @returns { boolean } The output returned by the function `isOverflowing()` is
* `true` if the width of the object is greater than 0 and false otherwise.
*/
    isOverflowing() {
      return this.getWidth() > 0;
    }

    // Private
/**
* @description This function disables the automatic vertical overflow of an element
* by setting its `overflow` style to `hidden`.
* 
* @returns { any } The output returned by `_disableOverflow()` is `undefined`.
* 
* This function sets the ` overflow` attribute of the element to `hidden`, effectively
* disabling scrolling on the element.
*/
    _disableOverFlow() {
      this._saveInitialAttribute(this._element, 'overflow');
      this._element.style.overflow = 'hidden';
    }
/**
* @description This function sets the style property of an element based on its
* current computed value and a callback function.
* 
* @param { string } selector - The `selector` input parameter specifies which elements
* should be targeted for manipulation. It is used to select specific elements based
* on their DOM selectors (e.g.
* 
* @param { string } styleProperty - The `styleProperty` input parameter specifies
* the CSS property that should be modified.
* 
* @param { number } callback - The `callback` function takes the calculated value
* of `styleProperty` and returns a pixel value to set as the final style for the element.
* 
* @returns { any } This function takes three arguments: `selector`, `styleProperty`,
* and `callback`. It returns nothing (undefined) because it is a void function.
* 
* The function manipulates the style of an element matching the given `selector` by
* setting the value of the given `styleProperty` to the return value of the `callback`
* function.
*/
    _setElementAttributes(selector, styleProperty, callback) {
      const scrollbarWidth = this.getWidth();
/**
* @description This function is a callback function for the `getComputedStyle()`
* method that calculates the pixels-width value of an HTML element's style property
* (based on the width of its containing block and scrollbar width).
* 
* @param { object } element - The `element` input parameter is the DOM element to
* which the style property will be applied.
* 
* @returns { any } The function takes an `element` parameter and returns no output
* (i.e., `undefined`).
*/
      const manipulationCallBack = element => {
        if (element !== this._element && window.innerWidth > element.clientWidth + scrollbarWidth) {
          return;
        }
        this._saveInitialAttribute(element, styleProperty);
        const calculatedValue = window.getComputedStyle(element).getPropertyValue(styleProperty);
        element.style.setProperty(styleProperty, `${callback(Number.parseFloat(calculatedValue))}px`);
      };
      this._applyManipulationCallback(selector, manipulationCallBack);
    }
/**
* @description This function saves the current value of an CSS style property to a
* data attribute on the element.
* 
* @param {  } element - The `element` input parameter is the HTML element for which
* the attribute value is being retrieved and saved as a data-attribute.
* 
* @param { string } styleProperty - The `styleProperty` input parameter passed to
* `_saveInitialAttribute()` function is a string representing a CSS property name (e.g.
* 
* @returns { any } This function takes an HTML element and a style property as inputs
* and sets the value of that property on the element using `element.style.setProperty()`.
* It then sets a data attribute on the element with the same value.
* 
* The output of the function is the current value of the style property for the
* element as set by `element.style.setProperty()`.
*/
    _saveInitialAttribute(element, styleProperty) {
      const actualValue = element.style.getPropertyValue(styleProperty);
      if (actualValue) {
        Manipulator.setDataAttribute(element, styleProperty, actualValue);
      }
    }
/**
* @description This function removes a CSS style property from an element if its
* value is `null`, otherwise it removes the property's data attribute and sets the
* property value back to the original value.
* 
* @param { string } selector - The `selector` input parameter is a CSS selector that
* selects the elements to which the function should apply the attribute removal and
* property setting.
* 
* @param { string } styleProperty - The `styleProperty` input parameter is the name
* of a CSS property that should be added or removed from an element based on its
* current value.
* 
* @returns {  } The function takes two parameters: `selector` and `styleProperty`.
* It removes a property from all elements matching the `selector`, if the value of
* that property is null. If the property does not exist on an element it sets that
* element to have no value for that style property.
*/
    _resetElementAttributes(selector, styleProperty) {
/**
* @description This function is a callback function for manipulate-element event.
* It gets the value of a certain style property of an element (through
* `Manipulator.getDataAttribute()`), and if that value is `null`, it removes the
* property using `element.style.removeProperty()`.
* 
* @param {  } element - The `element` input parameter is a DOMElement that the
* manipulation callback function will operate on.
* 
* @returns {  } This function takes an HTML element as input and performs the following
* operations:
* 
* 1/ It retrieves the value of a custom data attribute `styleProperty` from the
* element using `Manipulator.getDataAttribute()`.
* 2/ If the value is null or zero.
* 
* If true: Removes the style property from the element's CSS styles using `element.style.removeProperty()`
*      If false: Removes the custom data attribute from the element using `Manipulator.removeDataAttribute()`.
*/
      const manipulationCallBack = element => {
        const value = Manipulator.getDataAttribute(element, styleProperty);
        // We only want to remove the property if the value is `null`; the value can also be zero
        if (value === null) {
          element.style.removeProperty(styleProperty);
          return;
        }
        Manipulator.removeDataAttribute(element, styleProperty);
        element.style.setProperty(styleProperty, value);
      };
      this._applyManipulationCallback(selector, manipulationCallBack);
    }
/**
* @description This function takes a selector and a callback function as input.
* 
* @param { string } selector - In this function `selector` is the CSS selector that
* is passed as an argument.
* 
* @param {  } callBack - The `callback` parameter is a function that is passed to
* the `applyManipulationCallback` function.
* 
* @returns { any } The function `_applyManipulationCallback` takes two arguments:
* `selector` and `callBack`. It applies the callback to each element matched by the
* selector.
* 
* The output returned by this function is not explicitly defined because it does not
* return anything. Instead of returning a value from the function and letting its
* caller manage side effects/asynchronous behavior ( like animations ), the function
* takes over all asynchronous responsibilities of firing callbacks after elements
* matching a selector are collected with SelectorEngine.find(selector), making any
* callback passed here fire against the same collection . The function simply
* manipulates DOM elements and immediately calls the `callBack` function with each
* matching element; callBack has control of what follows or side effects as result
* . It effectively provides control over async responsibilities instead.
*/
    _applyManipulationCallback(selector, callBack) {
      if (isElement$1(selector)) {
        callBack(selector);
        return;
      }
      for (const sel of SelectorEngine.find(selector, this._element)) {
        callBack(sel);
      }
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap modal.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$7 = 'modal';
  const DATA_KEY$4 = 'bs.modal';
  const EVENT_KEY$4 = `.${DATA_KEY$4}`;
  const DATA_API_KEY$2 = '.data-api';
  const ESCAPE_KEY$1 = 'Escape';
  const EVENT_HIDE$4 = `hide${EVENT_KEY$4}`;
  const EVENT_HIDE_PREVENTED$1 = `hidePrevented${EVENT_KEY$4}`;
  const EVENT_HIDDEN$4 = `hidden${EVENT_KEY$4}`;
  const EVENT_SHOW$4 = `show${EVENT_KEY$4}`;
  const EVENT_SHOWN$4 = `shown${EVENT_KEY$4}`;
  const EVENT_RESIZE$1 = `resize${EVENT_KEY$4}`;
  const EVENT_CLICK_DISMISS = `click.dismiss${EVENT_KEY$4}`;
  const EVENT_MOUSEDOWN_DISMISS = `mousedown.dismiss${EVENT_KEY$4}`;
  const EVENT_KEYDOWN_DISMISS$1 = `keydown.dismiss${EVENT_KEY$4}`;
  const EVENT_CLICK_DATA_API$2 = `click${EVENT_KEY$4}${DATA_API_KEY$2}`;
  const CLASS_NAME_OPEN = 'modal-open';
  const CLASS_NAME_FADE$3 = 'fade';
  const CLASS_NAME_SHOW$4 = 'show';
  const CLASS_NAME_STATIC = 'modal-static';
  const OPEN_SELECTOR$1 = '.modal.show';
  const SELECTOR_DIALOG = '.modal-dialog';
  const SELECTOR_MODAL_BODY = '.modal-body';
  const SELECTOR_DATA_TOGGLE$2 = '[data-bs-toggle="modal"]';
  const Default$6 = {
    backdrop: true,
    focus: true,
    keyboard: true
  };
  const DefaultType$6 = {
    backdrop: '(boolean|string)',
    focus: 'boolean',
    keyboard: 'boolean'
  };

  /**
   * Class definition
   */

  class Modal extends BaseComponent {
/**
* @description This function is the constructor for a popup (specifically a Material
* Design bottom sheet), and it performs the following tasks:
* 
* 1/ Creates a dialog element using SelectorEngine.findOne()
* 2/ Initializes a backdrop element
* 3/ Initializes a focus trap
* 4/ Sets internal flags for _isShown and _isTransitioning to false
* 5/ Creates a scroll bar helper object
* 6/ Adds event listeners to the dialog element.
* 
* @param {  } element - The `element` input parameter is the container element that
* will host the dialog.
* 
* @param { object } config - The `config` input parameter is used to pass optional
* configuration values to the constructor of the widget. In this specific case of a
* modal window constructor with jQuery UI v1.12.1.14858 - which is what SELECTOR_DIALOG
* refers to), the parameters config has several values that affect functionality as
* defined by default by jQuery.
* For instance:
*   `classes`        A collection of space-separated string that classnames to apply
* to the new element. This parameter provides default className values used when
* initialising a dialog or its elements during the constructor creation cycle of the
* new dialog.
* One may modify this property to include custom class names that may enhance styles
* specific for their unique requirements; an example being:  `classes: 'modal modal-
* info'`.   This affects how the new created modal dialog will look visually onscreen
* for a web application. Others may modify according to requirement.
* Other optional parameters for config include`disabled`,`Modal`, and `templateString`.
* These allow greater flexibility during runtime or static design considerations.
* 
* All said above simply suggests the value held by 'config' allows passing customising
* choices available out-of-the-box. For details on these values you may use either
* the linked jQuery documentation(s), a Google search using related identifying
* descriptors such as  `jQuery modal confict` and read its respective descriptions
* on that site (especially with focus).
* That way instead of reiterating it all there.
* In simple words if your need modification/flexibility control when creating an
* element/ widget with a set parameters you want to customize before they get
* generated; just take those parameter suggestions available within the constructor
* call from `super()` as the primary parameter is actually provided by default already
* to start calling its parent and iterate (optional here anyhow.)   And then decide
* what modifications for default configuration makes most sense and feasibility and
* go ahead. These can then interact correctly during dynamic rendering phase on runtime.
* 
* @returns { object } This function returns a ` Dialog ` object.
*/
    constructor(element, config) {
      super(element, config);
      this._dialog = SelectorEngine.findOne(SELECTOR_DIALOG, this._element);
      this._backdrop = this._initializeBackDrop();
      this._focustrap = this._initializeFocusTrap();
      this._isShown = false;
      this._isTransitioning = false;
      this._scrollBar = new ScrollBarHelper();
      this._addEventListeners();
    }

    // Getters
/**
* @description This function is a getter method for a property called `Default` that
* returns a constant value `Default$6`.
* 
* @returns { object } The function returns `Default$6`, which is `undefined`.
*/
    static get Default() {
      return Default$6;
    }
/**
* @description This function returns a constant value called `DefaultType$6`.
* 
* @returns {  } The output returned by this function is `DefaultType$6`.
*/
    static get DefaultType() {
      return DefaultType$6;
    }
/**
* @description This function is a static method that returns the value of a private
* instance field named `NAME$.
* 
* @returns { string } The output of the function is "undefined". The function tries
* to access a variable called `NAME`, but it is not defined anywhere. The `$7` at
* the end of the function name suggests that it might be trying to access a static
* variable with the name `NAME`, but since there is no such variable declared anywhere
* and no static variables are defined by the code given above; nothing is found to
* return so null/undefined should be returned when you run the function.
*/
    static get NAME() {
      return NAME$7;
    }

    // Public
/**
* @description The `toggle()` function is a click handler that returns a function
* to hide or show the element based on its current visibility state.
* 
* @param { object } relatedTarget - The `relatedTarget` input parameter specifies
* the target element to which the Popper should be anchored when showing or hiding.
* 
* @returns { boolean } The output returned by the `toggle` function is a boolean
* value indicating whether the element should be hidden or shown based on its previous
* state. Specifically:
* 
* 	- If the element was previously shown (`this._isShown` was `true`), then the
* function returns `false`.
* 	- If the element was previously hidden (`this._isShowned` was `false]), then the
* function returns `true`.
* 
* In other words; when the `_isShown` property is set to `true`, and we call
* `toggle(relatedTarget)`, it will return `false`.
*/
    toggle(relatedTarget) {
      return this._isShown ? this.hide() : this.show(relatedTarget);
    }
/**
* @description This function shows a modal element (represented by `this`) and handles
* the `EVENT_SHOW$4` event.
* 
* @param { object } relatedTarget - The `relatedTarget` input parameter specifies
* the element that triggered the show event.
* 
* @returns { any } This function is a widget that shows and animates a popup
* (represented by the `_element` property). The output returned by this function is
* no error or default prevention of the show event. The function first checks if the
* popup is already shown or transitioning before executing any logic. If it is already
* shown or transitioning ,it returns immediately. If the show event is not default
* prevented and the element is not shown or transitioning ,it sets isShown to true
* and transitioning to true and hides the scroll bar. Finally  adds a class to the
* body tag indicating the popup is open. After this It animates the popup into view
* using its adjust dialog method. The _show element method takes a related target
* argument which can be used specify an element that is linked with the popup's opening.
*/
    show(relatedTarget) {
      if (this._isShown || this._isTransitioning) {
        return;
      }
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW$4, {
        relatedTarget
      });
      if (showEvent.defaultPrevented) {
        return;
      }
      this._isShown = true;
      this._isTransitioning = true;
      this._scrollBar.hide();
      document.body.classList.add(CLASS_NAME_OPEN);
      this._adjustDialog();
      this._backdrop.show(() => this._showElement(relatedTarget));
    }
/**
* @description This function hides a modal element by transitioning it from shown
* to hidden state.
* 
* @returns {  } The output returned by the `hide` function is undefined. The function
* does not return anything.
*/
    hide() {
      if (!this._isShown || this._isTransitioning) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE$4);
      if (hideEvent.defaultPrevented) {
        return;
      }
      this._isShown = false;
      this._isTransitioning = true;
      this._focustrap.deactivate();
      this._element.classList.remove(CLASS_NAME_SHOW$4);
      this._queueCallback(() => this._hideModal(), this._element, this._isAnimated());
    }
/**
* @description This function disposes of the event listeners and child elements of
* a dismissible Modal Dialog.
* 
* @returns {  } The output of this function is undefined.
*/
    dispose() {
      EventHandler.off(window, EVENT_KEY$4);
      EventHandler.off(this._dialog, EVENT_KEY$4);
      this._backdrop.dispose();
      this._focustrap.deactivate();
      super.dispose();
    }
/**
* @description This function updates the dialog layout based on changes to the
* interface elements.
* 
* @returns { any } The function `handleUpdate()` does not return any value explicitly.
* It has a syntax error since `this` is undefined.
*/
    handleUpdate() {
      this._adjustDialog();
    }

    // Private
/**
* @description This function initializes a new Backdrop object based on the configured
* settings.
* 
* @returns {  } The output returned by the `undefined` function is an instance of
* the `Backdrop` class with properties `isVisible` and `isAnimated`.
*/
    _initializeBackDrop() {
      return new Backdrop({
        isVisible: Boolean(this._config.backdrop),
        // 'static' option will be translated to true, and booleans will keep their value,
        isAnimated: this._isAnimated()
      });
    }
/**
* @description This function creates a new `FocusTrap` instance and returns it.
* 
* @returns { object } The ` undefined `_ initializeFocusTrap function returns an
* object of type `FocusTrap`, which is an instance of the FocusTrap constructor with
* its `trapElement` property set to `this._element`.
*/
    _initializeFocusTrap() {
      return new FocusTrap({
        trapElement: this._element
      });
    }
/**
* @description This function is handling the showing of a modal element (with class
* `ClassNameShow`). It appends the element to the body if it's not already there and
* displays it with CSS transition animations. If the focus has been set to move to
* the modal upon showning it also sets the focus using a `focustrap` object.
* 
* @param {  } relatedTarget - The `relatedTarget` input parameter is used to specify
* the element that triggered the show event.
* 
* @returns {  } The `showElement` function takes an element as a parameter and appends
* it to the body of the document if it doesn't already contain the element. It then
* sets the display property of the element to "block" and adds an "aria-modal"
* attribute with a value of true. The function also scrolls the top position of the
* element and any associated modal body element to 0.
*/
    _showElement(relatedTarget) {
      // try to append dynamic modal
      if (!document.body.contains(this._element)) {
        document.body.append(this._element);
      }
      this._element.style.display = 'block';
      this._element.removeAttribute('aria-hidden');
      this._element.setAttribute('aria-modal', true);
      this._element.setAttribute('role', 'dialog');
      this._element.scrollTop = 0;
      const modalBody = SelectorEngine.findOne(SELECTOR_MODAL_BODY, this._dialog);
      if (modalBody) {
        modalBody.scrollTop = 0;
      }
      reflow(this._element);
      this._element.classList.add(CLASS_NAME_SHOW$4);
/**
* @description This function is a transition completion callback that activates the
* focus trap if config.focus is set and triggers the shown event with the related target.
* 
* @returns { any } The output returned by this function is `undefined`. This function
* is an arrow function expressions and does not have a return statement.
*/
      const transitionComplete = () => {
        if (this._config.focus) {
          this._focustrap.activate();
        }
        this._isTransitioning = false;
        EventHandler.trigger(this._element, EVENT_SHOWN$4, {
          relatedTarget
        });
      };
      this._queueCallback(transitionComplete, this._dialog, this._isAnimated());
    }
/**
* @description This function adds event listeners to the dialog element and its
* parent window for various events such as keydown/, mousedown/, and resize/.
* 
* @returns { any } The output of this function is a set of event listeners that are
* attached to the dialog element and the window.
*/
    _addEventListeners() {
      EventHandler.on(this._element, EVENT_KEYDOWN_DISMISS$1, event => {
        if (event.key !== ESCAPE_KEY$1) {
          return;
        }
        if (this._config.keyboard) {
          this.hide();
          return;
        }
        this._triggerBackdropTransition();
      });
      EventHandler.on(window, EVENT_RESIZE$1, () => {
        if (this._isShown && !this._isTransitioning) {
          this._adjustDialog();
        }
      });
      EventHandler.on(this._element, EVENT_MOUSEDOWN_DISMISS, event => {
        // a bad trick to segregate clicks that may start inside dialog but end outside, and avoid listen to scrollbar clicks
        EventHandler.one(this._element, EVENT_CLICK_DISMISS, event2 => {
          if (this._element !== event.target || this._element !== event2.target) {
            return;
          }
          if (this._config.backdrop === 'static') {
            this._triggerBackdropTransition();
            return;
          }
          if (this._config.backdrop) {
            this.hide();
          }
        });
      });
    }
/**
* @description This function hides a modal and resets its styling and attributes.
* It sets the display property to "none", sets aria-hidden to true and removes other
* attributes such as aria-modal and role.
* 
* @returns {  } The `_hideModal()` function returns nothing (i.e., `undefined`) and
* has several side effects:
* 
* 1/ It sets the `display` style of the element to `'none'`.
* 2/ It sets the `aria-hidden` attribute to `true`.
* 3/ It removes the `aria-modal` attribute and the `role` attribute from the element.
* 4/ It sets the `isTransitioning` flag to `false`.
* 5/ It calls the `hide()` method on the backdrop element to hide it.
* 6/ It triggers the `hidden` event on the element.
*/
    _hideModal() {
      this._element.style.display = 'none';
      this._element.setAttribute('aria-hidden', true);
      this._element.removeAttribute('aria-modal');
      this._element.removeAttribute('role');
      this._isTransitioning = false;
      this._backdrop.hide(() => {
        document.body.classList.remove(CLASS_NAME_OPEN);
        this._resetAdjustments();
        this._scrollBar.reset();
        EventHandler.trigger(this._element, EVENT_HIDDEN$4);
      });
    }
/**
* @description This function checks if the element has a classlist containing the
* `CLASS_NAME_FADE` string.
* 
* @returns { boolean } This function `_isAnimated` returns a `bool` value indicating
* whether the element has the class `CLASS_NAME_FADE`.
*/
    _isAnimated() {
      return this._element.classList.contains(CLASS_NAME_FADE$3);
    }
/**
* @description This function triggers a background transition when the modal is
* hidden. It adds a class to the element to temporarily prevent layout shifts and
* then sets overflow to hide to prevent the content from being visible during the transition.
* 
* @returns {  } The output returned by `_triggerBackdropTransition()` is not specified
* because it's a void function (returns `undefined`). The function triggers events
* and performs styles changes to the element without returning anything.
*/
    _triggerBackdropTransition() {
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE_PREVENTED$1);
      if (hideEvent.defaultPrevented) {
        return;
      }
      const isModalOverflowing = this._element.scrollHeight > document.documentElement.clientHeight;
      const initialOverflowY = this._element.style.overflowY;
      // return if the following background transition hasn't yet completed
      if (initialOverflowY === 'hidden' || this._element.classList.contains(CLASS_NAME_STATIC)) {
        return;
      }
      if (!isModalOverflowing) {
        this._element.style.overflowY = 'hidden';
      }
      this._element.classList.add(CLASS_NAME_STATIC);
      this._queueCallback(() => {
        this._element.classList.remove(CLASS_NAME_STATIC);
        this._queueCallback(() => {
          this._element.style.overflowY = initialOverflowY;
        }, this._dialog);
      }, this._dialog);
      this._element.focus();
    }

    /**
     * The following methods are used to handle overflowing modals
     */

    _adjustDialog() {
      const isModalOverflowing = this._element.scrollHeight > document.documentElement.clientHeight;
      const scrollbarWidth = this._scrollBar.getWidth();
      const isBodyOverflowing = scrollbarWidth > 0;
      if (isBodyOverflowing && !isModalOverflowing) {
        const property = isRTL() ? 'paddingLeft' : 'paddingRight';
        this._element.style[property] = `${scrollbarWidth}px`;
      }
      if (!isBodyOverflowing && isModalOverflowing) {
        const property = isRTL() ? 'paddingRight' : 'paddingLeft';
        this._element.style[property] = `${scrollbarWidth}px`;
      }
    }
/**
* @description The provided function (`_resetAdjustments`) resets the padding left
* and right properties of the element to empty strings (`''`).
* 
* @returns { any } The output returned by the function is not defined because the
* function does not return anything.
*/
    _resetAdjustments() {
      this._element.style.paddingLeft = '';
      this._element.style.paddingRight = '';
    }

    // Static
/**
* @description This function is a jQuery interface for modal dialogs.
* 
* @param { object } config - The `config` input parameter is used to specify options
* or configuration for the modal instance. It can be a string representing the method
* name to call on the instance (e.g., 'show', 'hide') or an object with multiple
* configuration options.
* 
* @param {  } relatedTarget - The `relatedTarget` parameter is an optional input
* passed to the modal method that identifies the target element associated with the
* modal event triggering the method call.
* 
* @returns {  } The output of this function is a function that returns `this.each()`.
*/
    static jQueryInterface(config, relatedTarget) {
      return this.each(function () {
        const data = Modal.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config](relatedTarget);
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$2, SELECTOR_DATA_TOGGLE$2, function (event) {
    const target = SelectorEngine.getElementFromSelector(this);
    if (['A', 'AREA'].includes(this.tagName)) {
      event.preventDefault();
    }
    EventHandler.one(target, EVENT_SHOW$4, showEvent => {
      if (showEvent.defaultPrevented) {
        // only register focus restorer if modal will actually get shown
        return;
      }
      EventHandler.one(target, EVENT_HIDDEN$4, () => {
        if (isVisible(this)) {
          this.focus();
        }
      });
    });

    // avoid conflict when clicking modal toggler while another one is open
    const alreadyOpen = SelectorEngine.findOne(OPEN_SELECTOR$1);
    if (alreadyOpen) {
      Modal.getInstance(alreadyOpen).hide();
    }
    const data = Modal.getOrCreateInstance(target);
    data.toggle(this);
  });
  enableDismissTrigger(Modal);

  /**
   * jQuery
   */

  defineJQueryPlugin(Modal);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap offcanvas.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$6 = 'offcanvas';
  const DATA_KEY$3 = 'bs.offcanvas';
  const EVENT_KEY$3 = `.${DATA_KEY$3}`;
  const DATA_API_KEY$1 = '.data-api';
  const EVENT_LOAD_DATA_API$2 = `load${EVENT_KEY$3}${DATA_API_KEY$1}`;
  const ESCAPE_KEY = 'Escape';
  const CLASS_NAME_SHOW$3 = 'show';
  const CLASS_NAME_SHOWING$1 = 'showing';
  const CLASS_NAME_HIDING = 'hiding';
  const CLASS_NAME_BACKDROP = 'offcanvas-backdrop';
  const OPEN_SELECTOR = '.offcanvas.show';
  const EVENT_SHOW$3 = `show${EVENT_KEY$3}`;
  const EVENT_SHOWN$3 = `shown${EVENT_KEY$3}`;
  const EVENT_HIDE$3 = `hide${EVENT_KEY$3}`;
  const EVENT_HIDE_PREVENTED = `hidePrevented${EVENT_KEY$3}`;
  const EVENT_HIDDEN$3 = `hidden${EVENT_KEY$3}`;
  const EVENT_RESIZE = `resize${EVENT_KEY$3}`;
  const EVENT_CLICK_DATA_API$1 = `click${EVENT_KEY$3}${DATA_API_KEY$1}`;
  const EVENT_KEYDOWN_DISMISS = `keydown.dismiss${EVENT_KEY$3}`;
  const SELECTOR_DATA_TOGGLE$1 = '[data-bs-toggle="offcanvas"]';
  const Default$5 = {
    backdrop: true,
    keyboard: true,
    scroll: false
  };
  const DefaultType$5 = {
    backdrop: '(boolean|string)',
    keyboard: 'boolean',
    scroll: 'boolean'
  };

  /**
   * Class definition
   */

  class Offcanvas extends BaseComponent {
/**
* @description This constructor function is initializing a new instance of an object
* that extends a superclass (which is not shown here), and it does the following:
* 
* 	- Initializes the backdrop element using the `_initializeBackDrop` method.
* 	- Initializes the focus trap element using the `_initializeFocusTrap` method.
* 	- Adds event listeners using the `_addEventListeners` method.
* 
* Overall the function is setting up the initial state of the object and attaching
* event listeners for various events.
* 
* @param {  } element - The `element` input parameter is the HTML element that the
* constructor is being called on.
* 
* @param { object } config - The `config` input parameter is used to pass options
* or settings to the constructor of the widget.
* 
* @returns { Component } The function constructor(element、config) returns undefined，no
* explicit return statement exists.
*/
    constructor(element, config) {
      super(element, config);
      this._isShown = false;
      this._backdrop = this._initializeBackDrop();
      this._focustrap = this._initializeFocusTrap();
      this._addEventListeners();
    }

    // Getters
/**
* @description This function is a `static` getter method for a property called
* `Default` of the class that it belongs to.
* 
* @returns { object } The function `get Default()` returns `Default$5`, which is undefined.
*/
    static get Default() {
      return Default$5;
    }
/**
* @description This function is a static method that returns the `DefaultType`
* constant for the class.
* 
* @returns { number } The output returned by this function is `DefaultType$5`.
*/
    static get DefaultType() {
      return DefaultType$5;
    }
/**
* @description This function is a "getter" method that returns the value of the
* "NAME" variable.
* 
* @returns { string } The function returns `NAME$6`, which is `undefined` since
* `NAME` is not defined.
*/
    static get NAME() {
      return NAME$6;
    }

    // Public
/**
* @description The `toggle` function returns either the `hide()` method or the
* `show()` method depending on the current visibility state of the element.
* 
* @param {  } relatedTarget - The `relatedTarget` parameter is an optional element
* that the `toggle()` function uses as a reference point to position the dropdown
* correctly relative to the target element.
* 
* @returns {  } The output of the `toggle()` function is either the function's first
* argument (`relatedTarget`) if the component is shown and the `hide()` method is
* called on it (i.e., `this._isShown = true`), or the `relatedTarget` argument if
* the component is hidden and the `show()` method is called on it (i.e., `this._isShown
* = false`).
*/
    toggle(relatedTarget) {
      return this._isShown ? this.hide() : this.show(relatedTarget);
    }
/**
* @description This function is called "show" and it shows the popover. It sets
* various attributes on the element to indicate that it's being shown (aria-modal
* and role=dialog), adds a class to the element indicating it's showing , and triggers
* an event to signal that it's been shown. If scroll is enabled it hides the scroll
* bar helper.
* 
* @param { object } relatedTarget - The `relatedTarget` input parameter specifies
* the element that the modal is being shown for.
* 
* @returns {  } This function returns nothing (void) or undefined because it is not
* stated to return anything explicitly.
*/
    show(relatedTarget) {
      if (this._isShown) {
        return;
      }
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW$3, {
        relatedTarget
      });
      if (showEvent.defaultPrevented) {
        return;
      }
      this._isShown = true;
      this._backdrop.show();
      if (!this._config.scroll) {
        new ScrollBarHelper().hide();
      }
      this._element.setAttribute('aria-modal', true);
      this._element.setAttribute('role', 'dialog');
      this._element.classList.add(CLASS_NAME_SHOWING$1);
/**
* @description This function completes the animation of a dropdown menu's show event
* by adding CSS classes and triggering an event.
* 
* @returns {  } The output of the function `completeCallback` is not specified
* directly; it appears to be a side effect of executing the function's body.
* 
* Here's a breakdown of the code:
* 
* 1/ `if (!this._config.scroll || this._config.backdrop) {...}` - This condition
* checks if the `scroll` configuration is not set or if `backdrop` is set to true.
* If either condition is met (i.e., `scroll` is unset or `backdrop` is truthy), the
* function inside the block is executed.
* 2/ `this._focustrap.activate();` - This line activates the focus trap (whatever
* that means).
* 3/ `this._element.classList.add(CLASS_NAME_SHOW$3);`,
* `this._element.classList.remove(CLASS_NAME_SHOWING$1);` - These lines add and
* remove CSS classes from the `_element`.
* 4/ `EventHandler.trigger(this._element，EVENT_SHOWN$3，{ relatedTarget });` - This
* line triggers an event (specifically `EVENT_SHOWN$3`) on the `_element` with an
* options object containing a `relatedTarget` property.
* 
* Overall the function modifies the DOM and triggers events.
*/
      const completeCallBack = () => {
        if (!this._config.scroll || this._config.backdrop) {
          this._focustrap.activate();
        }
        this._element.classList.add(CLASS_NAME_SHOW$3);
        this._element.classList.remove(CLASS_NAME_SHOWING$1);
        EventHandler.trigger(this._element, EVENT_SHOWN$3, {
          relatedTarget
        });
      };
      this._queueCallback(completeCallBack, this._element, true);
    }
/**
* @description This function `hide()` hides the modal and performs other cleanup
* tasks. It checks if the modal is not already hidden and then triggers an event to
* deactivate the focustrap feature and hide the element and backdrop.
* 
* @returns {  } The `hide()` function of the Popper.js object returns nothing
* (undefined) as it is a void function.
*/
    hide() {
      if (!this._isShown) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE$3);
      if (hideEvent.defaultPrevented) {
        return;
      }
      this._focustrap.deactivate();
      this._element.blur();
      this._isShown = false;
      this._element.classList.add(CLASS_NAME_HIDING);
      this._backdrop.hide();
/**
* @description This function is the completion callback for a modal dialog box. It
* removes the CSS class names associated with the modal and resets the scroll bar helper.
* 
* @returns {  } This function's output (the return value of `completeCallback`) is
* not explicitly stated. Still looking at what occurs within completeCallBack yields
* the following insight:
* 
* The function performs these operations on this `_element`:
* 	- Remove CSS classes `CLASS_NAME_SHOW$3` and `CLASS_NAME_HIDING`.
* 	- Remove 'aria-modal' and 'role' attributes.
* 	- Triggers the event EVENT_HIDDEN$3 on this _element.
* 
* Summarily describing the function's output or return value: this function sets
* various styles and properties to `_element` and triggers an event called `EVENT_HIDDEN$3`.
*/
      const completeCallback = () => {
        this._element.classList.remove(CLASS_NAME_SHOW$3, CLASS_NAME_HIDING);
        this._element.removeAttribute('aria-modal');
        this._element.removeAttribute('role');
        if (!this._config.scroll) {
          new ScrollBarHelper().reset();
        }
        EventHandler.trigger(this._element, EVENT_HIDDEN$3);
      };
      this._queueCallback(completeCallback, this._element, true);
    }
/**
* @description This function is a disposal method for an object.
* 
* @returns {  } The `dispose()` function disposals several internal members (the
* `_backdrop` and `_focustrap` objects) before calling the `super.dispose()` method.
* The output of this function is empty (`undefined`) because there are no explicit
* returns statements and nothing is returned from the function.
*/
    dispose() {
      this._backdrop.dispose();
      this._focustrap.deactivate();
      super.dispose();
    }

    // Private
/**
* @description This function initializes a Backdrop element for a popover and sets
* its properties such as class name and visibility based on the configuration object
* passed to it.
* 
* @returns {  } The output of the function is a new Backdrop object. It has properties
* like className and rootElement that define its visual appearance and placement.
* The object also has an isVisible property which is set to true if the backdrop
* should be visible initially; if the user doesn't select a value for backdrop it
* defaults to true.
*/
    _initializeBackDrop() {
/**
* @description This function prepares to hide the modal by triggering an event if
* the backdrop is static.
* 
* @returns {  } The output of the `clickCallback` function is undefined. Here's why:
* 
* The function contains an if statement that checks whether the backdrop is set to
* "static". If it is set to static (i.e., true), the code inside the if statement
* is executed and EventHandler.trigger(this._element) is called with the
* EVENT_HIDE_PREVENTED event. Since there is no return statement inside the if block
* (and the return statement is outside the block), control will fall through to the
* line `this.hide();`, but no value is returned from the function.
*/
      const clickCallback = () => {
        if (this._config.backdrop === 'static') {
          EventHandler.trigger(this._element, EVENT_HIDE_PREVENTED);
          return;
        }
        this.hide();
      };

      // 'static' option will be translated to true, and booleans will keep their value
      const isVisible = Boolean(this._config.backdrop);
      return new Backdrop({
        className: CLASS_NAME_BACKDROP,
        isVisible,
        isAnimated: true,
        rootElement: this._element.parentNode,
        clickCallback: isVisible ? clickCallback : null
      });
    }
/**
* @description This function creates a new instance of the `FocusTrap` class with
* the `trapElement` property set to the current element.
* 
* @returns { object } The ` _initializeFocusTrap` function returns an instance of
* the `FocusTrap` class with the `trapElement` property set to `this._element`.
* 
* In simpler terms: It creates a new object that will manage the focus state of the
* element referenced by `this._element`.
*/
    _initializeFocusTrap() {
      return new FocusTrap({
        trapElement: this._element
      });
    }
/**
* @description This function adds event listeners for the `keydown` and `hide` events
* on an element with ID `this._element`.
* 
* @returns {  } The output of this function is None.
* 
* The function adds an event listener to the element with the EventHandler.on method.
* The event listener listens for the EVENT_KEYDOWN_DISMISS event and triggers a
* specific action when it is detected.
*/
    _addEventListeners() {
      EventHandler.on(this._element, EVENT_KEYDOWN_DISMISS, event => {
        if (event.key !== ESCAPE_KEY) {
          return;
        }
        if (this._config.keyboard) {
          this.hide();
          return;
        }
        EventHandler.trigger(this._element, EVENT_HIDE_PREVENTED);
      });
    }

    // Static
/**
* @description This function is a jQuery plugin interface for Offcanvas widget. It
* iterates through each matched element and creates or gets an instance of Offcanvas
* using the provided configuration. If the configuration method name does not exist
* or starts with underscore or is equal to 'constructor', it throws a TypeError.
* 
* @param { object } config - The `config` parameter is an options object that is
* passed to the instance of the Offcanvas component.
* 
* @returns {  } The function `static jQueryInterface(config)` returns `this` after
* iterating over each element and executing a configuration method on each one if
* the config is not a string or does not have an existing instance.
*/
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Offcanvas.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config](this);
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$1, SELECTOR_DATA_TOGGLE$1, function (event) {
    const target = SelectorEngine.getElementFromSelector(this);
    if (['A', 'AREA'].includes(this.tagName)) {
      event.preventDefault();
    }
    if (isDisabled(this)) {
      return;
    }
    EventHandler.one(target, EVENT_HIDDEN$3, () => {
      // focus on trigger when it is closed
      if (isVisible(this)) {
        this.focus();
      }
    });

    // avoid conflict when clicking a toggler of an offcanvas, while another is open
    const alreadyOpen = SelectorEngine.findOne(OPEN_SELECTOR);
    if (alreadyOpen && alreadyOpen !== target) {
      Offcanvas.getInstance(alreadyOpen).hide();
    }
    const data = Offcanvas.getOrCreateInstance(target);
    data.toggle(this);
  });
  EventHandler.on(window, EVENT_LOAD_DATA_API$2, () => {
    for (const selector of SelectorEngine.find(OPEN_SELECTOR)) {
      Offcanvas.getOrCreateInstance(selector).show();
    }
  });
  EventHandler.on(window, EVENT_RESIZE, () => {
    for (const element of SelectorEngine.find('[aria-modal][class*=show][class*=offcanvas-]')) {
      if (getComputedStyle(element).position !== 'fixed') {
        Offcanvas.getOrCreateInstance(element).hide();
      }
    }
  });
  enableDismissTrigger(Offcanvas);

  /**
   * jQuery
   */

  defineJQueryPlugin(Offcanvas);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/sanitizer.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  // js-docs-start allow-list
  const ARIA_ATTRIBUTE_PATTERN = /^aria-[\w-]*$/i;
  const DefaultAllowlist = {
    // Global attributes allowed on any supplied element below.
    '*': ['class', 'dir', 'id', 'lang', 'role', ARIA_ATTRIBUTE_PATTERN],
    a: ['target', 'href', 'title', 'rel'],
    area: [],
    b: [],
    br: [],
    col: [],
    code: [],
    div: [],
    em: [],
    hr: [],
    h1: [],
    h2: [],
    h3: [],
    h4: [],
    h5: [],
    h6: [],
    i: [],
    img: ['src', 'srcset', 'alt', 'title', 'width', 'height'],
    li: [],
    ol: [],
    p: [],
    pre: [],
    s: [],
    small: [],
    span: [],
    sub: [],
    sup: [],
    strong: [],
    u: [],
    ul: []
  };
  // js-docs-end allow-list

  const uriAttributes = new Set(['background', 'cite', 'href', 'itemtype', 'longdesc', 'poster', 'src', 'xlink:href']);

  /**
   * A pattern that recognizes URLs that are safe wrt. XSS in URL navigation
   * contexts.
   *
   * Shout-out to Angular https://github.com/angular/angular/blob/15.2.8/packages/core/src/sanitization/url_sanitizer.ts#L38
   */
  // eslint-disable-next-line unicorn/better-regex
  const SAFE_URL_PATTERN = /^(?!javascript:)(?:[a-z0-9+.-]+:|[^&:/?#]*(?:[/?#]|$))/i;
/**
* @description This function takes two arguments: `allowedAttributeList` and
* `uriAttributes`, and it returns a function that tests whether an HTML attribute
* is allowed or not. The function first checks if the attribute name is present on
* the `allowedAttributeList`. If so:
* 
* 1/ If the attribute's value is a URL (based on a test against the `SAFE_URL_PATTERN`
* RegExp), then the function returns `true`.
* 2/ Otherwise (if the attribute's value is not a URL), it checks if there is a
* RegExp match for the attribute name among the elements of `allowedAttributeList`.
* 
* @param { object } attribute - The `attribute` input parameter is passed to the
* function and represents an HTML attribute to be checked for allowability.
* 
* @param { array } allowedAttributeList - The `allowedAttributeList` input parameter
* is a list of allowed attribute names that are allowed to be present on the element.
* 
* @returns { boolean } This function takes an `attribute` and an `allowedAttributeList`,
* and returns a boolean value indicating whether the attribute is allowed or not.
* 
* The function first checks if the attribute name is present among the allowed
* attributes listed. If it is found to be a listed attribute then another check
* happens. The check will run if the current element has URI attributes. Then it
* makes another check by checking for a specific regular expression that defines
* whether that specific attribute contains the required pattern or not using `some`
* method of an array returned from `filter()` with array methods used within the
* function is indeed an array made only of RegExp type objects. This function returns
* true or false based on those conditions  mentioned above about which you're looking
* for; no output value assigned explicitly.
*/
  const allowedAttribute = (attribute, allowedAttributeList) => {
    const attributeName = attribute.nodeName.toLowerCase();
    if (allowedAttributeList.includes(attributeName)) {
      if (uriAttributes.has(attributeName)) {
        return Boolean(SAFE_URL_PATTERN.test(attribute.nodeValue));
      }
      return true;
    }

    // Check if a regular expression validates the attribute.
    return allowedAttributeList.filter(attributeRegex => attributeRegex instanceof RegExp).some(regex => regex.test(attributeName));
  };
/**
* @description This function sanitizes potentially harmful HTML content by removing
* any elements or attributes that are not whitelisted. It takes three parameters:
* 
* 	- `unsafeHtml`: the unsafe HTML content to be sanitized
* 	- `allowList`: a list of allowed element names and attributes
* 	- `sanitizeFunction`: an optional function to further customize the sanitization
* process.
* 
* The function first parses the given HTML string into a document object using
* `DOMParser`. Then it iterates over all elements and attributes inside the document
* body and checks if they are allowed using the `allowList`. If any element or
* attribute is not allowed it is removed from the document.
* 
* @param { string } unsafeHtml - The `unsafeHtml` input parameter is the HTML content
* that needs to be sanitized and processed for any harmful or unwanted content.
* 
* @param { object } allowList - The `allowList` input parameter is an object that
* specifies which HTML elements and attributes are allowed to be used within the
* unsafe HTML string. The function checks if each element and attribute found within
* the unsanitized HTML string matches one of the allowlisted items or not.
* 
* @param {  } sanitizeFunction - The `sanitizeFunction` input parameter allows the
* function to use a custom sanitization function instead of the default sanitization
* process.
* 
* @returns { string } This function takes three arguments: unsafe HTML content as a
* string (unsafeHtml), an allowlist of DOM elements and attributes as an object
* (allowList), and an optional sanitization function as a function reference (sanitizeFunction).
* 
* It returns the sanitized HTML content as a string. Here's a concise description
* of the output:
* 
* The function parses the input HTML string using the DOMParser API and removes any
* elements or attributes that are not permitted by the allowlist.
*/
  function sanitizeHtml(unsafeHtml, allowList, sanitizeFunction) {
    if (!unsafeHtml.length) {
      return unsafeHtml;
    }
    if (sanitizeFunction && typeof sanitizeFunction === 'function') {
      return sanitizeFunction(unsafeHtml);
    }
    const domParser = new window.DOMParser();
    const createdDocument = domParser.parseFromString(unsafeHtml, 'text/html');
    const elements = [].concat(...createdDocument.body.querySelectorAll('*'));
    for (const element of elements) {
      const elementName = element.nodeName.toLowerCase();
      if (!Object.keys(allowList).includes(elementName)) {
        element.remove();
        continue;
      }
      const attributeList = [].concat(...element.attributes);
      const allowedAttributes = [].concat(allowList['*'] || [], allowList[elementName] || []);
      for (const attribute of attributeList) {
        if (!allowedAttribute(attribute, allowedAttributes)) {
          element.removeAttribute(attribute.nodeName);
        }
      }
    }
    return createdDocument.body.innerHTML;
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/template-factory.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$5 = 'TemplateFactory';
  const Default$4 = {
    allowList: DefaultAllowlist,
    content: {},
    // { selector : text ,  selector2 : text2 , }
    extraClass: '',
    html: false,
    sanitize: true,
    sanitizeFn: null,
    template: '<div></div>'
  };
  const DefaultType$4 = {
    allowList: 'object',
    content: 'object',
    extraClass: '(string|function)',
    html: 'boolean',
    sanitize: 'boolean',
    sanitizeFn: '(null|function)',
    template: 'string'
  };
  const DefaultContentType = {
    entry: '(string|element|function|null)',
    selector: '(string|element)'
  };

  /**
   * Class definition
   */

  class TemplateFactory extends Config {
/**
* @description This is a constructor function for an object that initializes the
* object with the properties and methods definedin the `config` object.
* 
* @param { object } config - The `config` input parameter is used to pass configuration
* options to the constructor.
* 
* @returns { object } The output returned by this function is `undefined`. This is
* because the `super()` call at the beginning of the constructor does not have a
* valid `this` context yet.
*/
    constructor(config) {
      super();
      this._config = this._getConfig(config);
    }

    // Getters
/**
* @description This function returns the value of the `Default` constant.
* 
* @returns {  } The output of the function `Default` is `Default$4`.
*/
    static get Default() {
      return Default$4;
    }
/**
* @description This function returns a constant value called `DefaultType$4`.
* 
* @returns { string } The function `getDefaultType` returns the value of `DefaultType$4`,
* which is `undefined`.
*/
    static get DefaultType() {
      return DefaultType$4;
    }
/**
* @description This function is a "getter" method that returns the value of a private
* static variable named `NAME$5`.
* 
* @returns { string } The function `getName` returns the value of the `NAME$5`
* variable. Since `NAME$5` is undefined and does not have a value assigned to it yet
* so will returning undefined.
*/
    static get NAME() {
      return NAME$5;
    }

    // Public
/**
* @description This function returns an array of possible functions (i.e., values
* that are not `undefined`) from the `content` object using `Object.values()`, maps
* each value to a resolved function using `this._resolvePossibleFunction()`., and
* filters out any `falsey` values using `filter(Boolean)`.
* 
* @returns { array } The `getContent()` function takes an object of configuration
* values as input and returns an array of possible function return values (evaluated
* using `this._resolvePossibleFunction()`) that are truthy (i.e., not `false` or
* `null`) after resolving any promise chains.
*/
    getContent() {
      return Object.values(this._config.content).map(config => this._resolvePossibleFunction(config)).filter(Boolean);
    }
/**
* @description This function checks if the `content` property of the object has a
* length greater than 0. In other words.
* 
* @returns { boolean } The output returned by this function is `false`. The function
* checks if the `content` property of the object is not empty (`length > 0`) and
* returns `true` if it is not empty and `false` otherwise.
*/
    hasContent() {
      return this.getContent().length > 0;
    }
/**
* @description This function called `changeContent` updates the `content` property
* of the object's configuration by combining the existing content with the provided
* `content` parameter.
* 
* @param { object } content - In this function `content` is an object that contains
* new properties to be merged into the existing `content` property of the instance's
* configuration.
* 
* @returns { object } Based on the provided code snippet:
* 
* The `changeContent` function takes a content parameter and updates the `content`
* property of the current configuration object with an object merged from the current
* config's `content` property and the new content parameter.
*/
    changeContent(content) {
      this._checkContent(content);
      this._config.content = {
        ...this._config.content,
        ...content
      };
      return this;
    }
/**
* @description This function takes a configuration object and a maybeSanitize function
* as parameters and returns a DOM element of type 'div' containing the configured
* content wrapped within it. The template div is created by assigning an innerHTML
* to a wrapper div and then looping over content Selectors and their corresponding
* text values and setting them using those selectors.
* 
* @returns {  } The `toHtml` function takes a configuration object and returns the
* HTML content rendered using that configuration.
*/
    toHtml() {
      const templateWrapper = document.createElement('div');
      templateWrapper.innerHTML = this._maybeSanitize(this._config.template);
      for (const [selector, text] of Object.entries(this._config.content)) {
        this._setContent(templateWrapper, text, selector);
      }
      const template = templateWrapper.children[0];
      const extraClass = this._resolvePossibleFunction(this._config.extraClass);
      if (extraClass) {
        template.classList.add(...extraClass.split(' '));
      }
      return template;
    }

    // Private
/**
* @description This function checks the types of the properties of a configuration
* object named "config".
* 
* @param { object } config - The `config` input parameter is used to pass a configuration
* object that contains the content to be checked for type errors.
* 
* @returns { object } The function `_typeCheckConfig` does not return anything (it
* has no `return` statement).
*/
    _typeCheckConfig(config) {
      super._typeCheckConfig(config);
      this._checkContent(config.content);
    }
/**
* @description This function iterates over the object `arg` and calls a type-checking
* method for each key-value pair.
* 
* @param { object } arg - The `arg` parameter is an object that contains a set of
* key-value pairs representing configuration options for the function.
* 
* @returns {  } This function takes an object as an argument and iterates through
* its properties (keys and values) using Object.entries(). For each property (selector
* and content), it calls the superclass's _typeCheckConfig method with the respective
* arguments: selector and content.
* 
* The output returned by this function is not explicitly defined; it depends on how
* the parent class (super) implements the _typeCheckConfig method. However based on
* the name of the method "defaultContentType" we can assume that this function might
* be checking if the content type of the passed config entry is correct or not.
*/
    _checkContent(arg) {
      for (const [selector, content] of Object.entries(arg)) {
        super._typeCheckConfig({
          selector,
          entry: content
        }, DefaultContentType);
      }
    }
/**
* @description This function sets the content of an element matching a selector
* within a template.
* 
* @param {  } template - The `template` input parameter is a reference to the HTML
* template element that should be populated with the content provided.
* 
* @param { string } content - Based on the function signature and the comments inside
* the function body:
* 
* The `content` input parameter specifies the inner HTML or text content that will
* be placed within the element selected by the `selector`.
* 
* @param { string } selector - The `selector` input parameter is a CSS selector used
* to locate a specific element within the template that will be filled with the given
* `content`.
* 
* @returns { string } This function takes three arguments: `template`, `content`,
* and `selector`. It selects the element matching `selector` within the `template`
* element using SelectorEngine.findOne(), and then sets the `content` as the innerHTML
* or textContent of that element.
* 
* The output of this function is not defined explicitly. Instead of returning anything
* directly to the caller (since there is no explicit return statement), it updates
* the content of the element selected by the `selector`.
*/
    _setContent(template, content, selector) {
      const templateElement = SelectorEngine.findOne(selector, template);
      if (!templateElement) {
        return;
      }
      content = this._resolvePossibleFunction(content);
      if (!content) {
        templateElement.remove();
        return;
      }
      if (isElement$1(content)) {
        this._putElementInTemplate(getElement(content), templateElement);
        return;
      }
      if (this._config.html) {
        templateElement.innerHTML = this._maybeSanitize(content);
        return;
      }
      templateElement.textContent = content;
    }
/**
* @description The `maybeSanitize` function sanitizes HTML input by removing any
* tags or content that are not allowed by the configuration object (`this._config`).
* 
* @param { string } arg - The `arg` input parameter is the input string that needs
* to be sanitized.
* 
* @returns { string } The function takes an `arg` argument and returns its output
* sanitized using HTML sanitization.
*/
    _maybeSanitize(arg) {
      return this._config.sanitize ? sanitizeHtml(arg, this._config.allowList, this._config.sanitizeFn) : arg;
    }
/**
* @description This function is a fallback resolution method for functions that are
* not found or are undefined. It takes an argument `arg` and executes it with the
* context of the current scope (represented by `[this]`).
* 
* @param { any } arg - The `arg` input parameter is passed as an argument to the
* function when it is called. It is not used within the function body and is instead
* passed directly to the `execute()` function that is being called within the `resolvePossibleFunction()`.
* 
* @returns {  } The output of this function would be `execute(arg,[this])`. It is
* executing `arg` with the single argument `[this]`.
*/
    _resolvePossibleFunction(arg) {
      return execute(arg, [this]);
    }
/**
* @description The function `_putElementInTemplate()` takes two elements `element`
* and `templateElement`, and puts the content of `element` into the innerHTML of `templateElement`.
* 
* @param { object } element - The `element` input parameter is the HTML element that
* should be inserted into the template Element.
* 
* @param {  } templateElement - In the provided function `_putElementInTemplate()`,
* the `templateElement` parameter is used to reference the existing element within
* the template that should be populated with the new content provided by the `element`
* parameter.
* 
* @returns { any } The function `_putElementInTemplate` takes two arguments `element`
* and `templateElement`, and it does not return any value.
*/
    _putElementInTemplate(element, templateElement) {
      if (this._config.html) {
        templateElement.innerHTML = '';
        templateElement.append(element);
        return;
      }
      templateElement.textContent = element.textContent;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap tooltip.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$4 = 'tooltip';
  const DISALLOWED_ATTRIBUTES = new Set(['sanitize', 'allowList', 'sanitizeFn']);
  const CLASS_NAME_FADE$2 = 'fade';
  const CLASS_NAME_MODAL = 'modal';
  const CLASS_NAME_SHOW$2 = 'show';
  const SELECTOR_TOOLTIP_INNER = '.tooltip-inner';
  const SELECTOR_MODAL = `.${CLASS_NAME_MODAL}`;
  const EVENT_MODAL_HIDE = 'hide.bs.modal';
  const TRIGGER_HOVER = 'hover';
  const TRIGGER_FOCUS = 'focus';
  const TRIGGER_CLICK = 'click';
  const TRIGGER_MANUAL = 'manual';
  const EVENT_HIDE$2 = 'hide';
  const EVENT_HIDDEN$2 = 'hidden';
  const EVENT_SHOW$2 = 'show';
  const EVENT_SHOWN$2 = 'shown';
  const EVENT_INSERTED = 'inserted';
  const EVENT_CLICK$1 = 'click';
  const EVENT_FOCUSIN$1 = 'focusin';
  const EVENT_FOCUSOUT$1 = 'focusout';
  const EVENT_MOUSEENTER = 'mouseenter';
  const EVENT_MOUSELEAVE = 'mouseleave';
  const AttachmentMap = {
    AUTO: 'auto',
    TOP: 'top',
    RIGHT: isRTL() ? 'left' : 'right',
    BOTTOM: 'bottom',
    LEFT: isRTL() ? 'right' : 'left'
  };
  const Default$3 = {
    allowList: DefaultAllowlist,
    animation: true,
    boundary: 'clippingParents',
    container: false,
    customClass: '',
    delay: 0,
    fallbackPlacements: ['top', 'right', 'bottom', 'left'],
    html: false,
    offset: [0, 6],
    placement: 'top',
    popperConfig: null,
    sanitize: true,
    sanitizeFn: null,
    selector: false,
    template: '<div class="tooltip" role="tooltip">' + '<div class="tooltip-arrow"></div>' + '<div class="tooltip-inner"></div>' + '</div>',
    title: '',
    trigger: 'hover focus'
  };
  const DefaultType$3 = {
    allowList: 'object',
    animation: 'boolean',
    boundary: '(string|element)',
    container: '(string|element|boolean)',
    customClass: '(string|function)',
    delay: '(number|object)',
    fallbackPlacements: 'array',
    html: 'boolean',
    offset: '(array|string|function)',
    placement: '(string|function)',
    popperConfig: '(null|object|function)',
    sanitize: 'boolean',
    sanitizeFn: '(null|function)',
    selector: '(string|boolean)',
    template: 'string',
    title: '(string|element|function)',
    trigger: 'string'
  };

  /**
   * Class definition
   */

  class Tooltip extends BaseComponent {
/**
* @description This function is a constructor for an object that represents a tooltip
* element.
* 
* @param {  } element - The `element` input parameter passes the DOM element on which
* the tooltip will be initialized.
* 
* @param { object } config - The `config` input parameter is used to define configuration
* options for the Tooltip instance.
* 
* @returns { object } The output of this function is a new object that has several
* properties and methods related to Bootstrap's tooltips.
* 
* Here is a brief description of each property and method:
* 
* 	- `tip`: The actual tooltip element that will be shown.
* 	- `_setListeners`: A method that sets event listeners for the element and its
* descendants to handle the triggering of the tooltip.
* 	- `_fixTitle`: A method that fixes the title of the tooltip if no selector is provided.
* 	- `_isEnabled`: A private property that indicates whether the tooltip is enabled
* or disabled.
* 	- `_timeout`: A private property that holds the timeout value for showing/hiding
* the tooltip.
* 	- `_isHovered`: A private property that indicates whether the user is currently
* hovering over the element that triggers the tooltip.
* 	- `_activeTrigger`: A private property that stores the active trigger (element
* or text) that caused the tooltip to be shown.
* 	- `_popper`: A private property that stores the Popper object that is used to
* position the tooltip.
* 	- `_templateFactory`: A private property that is used to create a new template
* for the tooltip content.
* 	- `_newContent`: A private property that holds the new content for the tooltip.
*/
    constructor(element, config) {
      if (typeof Popper === 'undefined') {
        throw new TypeError('Bootstrap\'s tooltips require Popper (https://popper.js.org)');
      }
      super(element, config);

      // Private
      this._isEnabled = true;
      this._timeout = 0;
      this._isHovered = null;
      this._activeTrigger = {};
      this._popper = null;
      this._templateFactory = null;
      this._newContent = null;

      // Protected
      this.tip = null;
      this._setListeners();
      if (!this._config.selector) {
        this._fixTitle();
      }
    }

    // Getters
/**
* @description This function returns the value of the `Default` constant.
* 
* @returns { number } The function has no definition for `Default`, so it returns `undefined`.
*/
    static get Default() {
      return Default$3;
    }
/**
* @description This function returns a constant value called `DefaultType$3`.
* 
* @returns { number } The output returned by the function is `DefaultType$3`.
*/
    static get DefaultType() {
      return DefaultType$3;
    }
/**
* @description This is agetter function that returns the value of the `NAME` property
* of the object.
* 
* @returns { string } The output returned by this function is "NAME$4".
*/
    static get NAME() {
      return NAME$4;
    }

    // Public
/**
* @description This function enables the object by setting its `_isEnabled` property
* to `true`.
* 
* @returns { boolean } This function does not return anything and has no output.
*/
    enable() {
      this._isEnabled = true;
    }
/**
* @description The function `disable()` sets the `_isEnabled` property of the object
* to `false`, which disables the object.
* 
* @returns { any } The function `disable()` sets the `isEnabled` property of the
* object to `false`.
* 
* The output of this function is `undefined`, because there is no explicit return statement.
*/
    disable() {
      this._isEnabled = false;
    }
/**
* @description The `toggleEnabled()` function flips the enabled status of the object
* (i.e., switching between `true` and `false`) without any effect on any other
* properties or states.
* 
* @returns {  } The output returned by `toggleEnabled()` is the opposite of its input
* value.
* 
* If `toggleEnabled()` is called with `true` as its argument:
* 
* 	- If `this._isEnabled` was previously `false`, it will be set to `true`.
* 	- If `this._isEnabled` was previously `true`, it will be set to `false`.
* 
* In other words.
*/
    toggleEnabled() {
      this._isEnabled = !this._isEnabled;
    }
/**
* @description This function toggles the visibility of an element based on a trigger
* click event.
* 
* @returns { object } This function takes no arguments and has no return statement.
* It first checks if the `this._isEnabled` property is falsey and returns immediately
* if so. If it's truthy (i.e., `this._isEnabled` is true), it sets the `click`
* property of the `_activeTrigger` property to its negation (`!..._activeTrigger.click`).
* If the function is called on a shown instance (i.e., `this._isShown() returns
* true`), it calls `this._leave()`, then sets `this._enter()`.
*/
    toggle() {
      if (!this._isEnabled) {
        return;
      }
      this._activeTrigger.click = !this._activeTrigger.click;
      if (this._isShown()) {
        this._leave();
        return;
      }
      this._enter();
    }
/**
* @description This function `dispose()` does the following:
* 
* 1/ Clears a timeout reference (`this._timeout`) using `clearTimeout()`.
* 2/ Removes an event listener for `EVENT_MODAL_HIDE` from the modal element's closest
* parent with the selector `SELECTOR_MODAL`.
* 3/ Restores the original title attribute of the modal element if it had one.
* 4/ Disposes the popper instance (if it exists).
* 5/ Calls the `super.dispose()` method.
* 
* @returns {  } The output returned by the `dispose()` function is undefined.
*/
    dispose() {
      clearTimeout(this._timeout);
      EventHandler.off(this._element.closest(SELECTOR_MODAL), EVENT_MODAL_HIDE, this._hideModalHandler);
      if (this._element.getAttribute('data-bs-original-title')) {
        this._element.setAttribute('title', this._element.getAttribute('data-bs-original-title'));
      }
      this._disposePopper();
      super.dispose();
    }
/**
* @description This function shows an element and positions it using a popper library.
* It checks if the element is currently hidden or not visible before throwing an error.
* 
* @returns { any } The `show` function returns nothing (undefined) because it is a
* void function. It primarily modifies the state of the button and attaches event
* listeners to its element and body elements.
*/
    show() {
      if (this._element.style.display === 'none') {
        throw new Error('Please use show on visible elements');
      }
      if (!(this._isWithContent() && this._isEnabled)) {
        return;
      }
      const showEvent = EventHandler.trigger(this._element, this.constructor.eventName(EVENT_SHOW$2));
      const shadowRoot = findShadowRoot(this._element);
      const isInTheDom = (shadowRoot || this._element.ownerDocument.documentElement).contains(this._element);
      if (showEvent.defaultPrevented || !isInTheDom) {
        return;
      }

      // TODO: v6 remove this or make it optional
      this._disposePopper();
      const tip = this._getTipElement();
      this._element.setAttribute('aria-describedby', tip.getAttribute('id'));
      const {
        container
      } = this._config;
      if (!this._element.ownerDocument.documentElement.contains(this.tip)) {
        container.append(tip);
        EventHandler.trigger(this._element, this.constructor.eventName(EVENT_INSERTED));
      }
      this._popper = this._createPopper(tip);
      tip.classList.add(CLASS_NAME_SHOW$2);

      // If this is a touch-enabled device we add extra
      // empty mouseover listeners to the body's immediate children;
      // only needed because of broken event delegation on iOS
      // https://www.quirksmode.org/blog/archives/2014/02/mouse_event_bub.html
      if ('ontouchstart' in document.documentElement) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.on(element, 'mouseover', noop);
        }
      }
/**
* @description This function sets the `isHovered` property to `false`, triggers an
* event called `EVENT_SHOWN$2`, and then calls the `leave()` method if `isHovered`
* is `false`.
* 
* @returns { any } The function complete() is a callback function that is triggered
* when an element is shown (i.e., displayed or visible).
*/
      const complete = () => {
        EventHandler.trigger(this._element, this.constructor.eventName(EVENT_SHOWN$2));
        if (this._isHovered === false) {
          this._leave();
        }
        this._isHovered = false;
      };
      this._queueCallback(complete, this.tip, this._isAnimated());
    }
/**
* @description The `hide()` function hides the popover ( tip ) element by removing
* its visibility and any event listeners that were added to the body elements to
* support iOS interactions.
* 
* @returns {  } The `hide()` function of the `Popover` class takes a variety of
* arguments and returns no value. It removes the popover's visible display and listens
* for various events to clean up its DOM elements and attributes.
*/
    hide() {
      if (!this._isShown()) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, this.constructor.eventName(EVENT_HIDE$2));
      if (hideEvent.defaultPrevented) {
        return;
      }
      const tip = this._getTipElement();
      tip.classList.remove(CLASS_NAME_SHOW$2);

      // If this is a touch-enabled device we remove the extra
      // empty mouseover listeners we added for iOS support
      if ('ontouchstart' in document.documentElement) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.off(element, 'mouseover', noop);
        }
      }
      this._activeTrigger[TRIGGER_CLICK] = false;
      this._activeTrigger[TRIGGER_FOCUS] = false;
      this._activeTrigger[TRIGGER_HOVER] = false;
      this._isHovered = null; // it is a trick to support manual triggering

/**
* @description This function `complete` is a lifecycle hook for a Popper element
* that removes the aria-describedby attribute from the element and triggers an event
* called EVENT_HIDDEN$2.
* 
* @returns { any } This function returns nothing (i.e., `undefined`) as it does not
* have a return statement.
*/
      const complete = () => {
        if (this._isWithActiveTrigger()) {
          return;
        }
        if (!this._isHovered) {
          this._disposePopper();
        }
        this._element.removeAttribute('aria-describedby');
        EventHandler.trigger(this._element, this.constructor.eventName(EVENT_HIDDEN$2));
      };
      this._queueCallback(complete, this.tip, this._isAnimated());
    }
/**
* @description The `update()` function updates the position of an element using the
* Popper library by calling `_popper.update()`.
* 
* @returns {  } This function does not return any value explicitly.
*/
    update() {
      if (this._popper) {
        this._popper.update();
      }
    }

    // Protected
/**
* @description This function checks if the `this` object has a `title` property with
* non-empty value (i.e., not `undefined`)
* 
* @returns { boolean } This function takes no arguments and returns a boolean value.
* The return value is determined by the existence of a title attribute within the
* current object.
*/
    _isWithContent() {
      return Boolean(this._getTitle());
    }
/**
* @description This function creates and returns a tip element if one does not already
* exist.
* 
* @returns {  } The output returned by this function is `this.tip` which is a reference
* to an HTML element representing the tooltip.
*/
    _getTipElement() {
      if (!this.tip) {
        this.tip = this._createTipElement(this._newContent || this._getContentForTemplate());
      }
      return this.tip;
    }
/**
* @description This function creates a tip element based on a provided content and
* adds the necessary CSS classes and ID to the element.
* 
* @param { string } content - The `content` input parameter provides the content to
* be displayed inside the tip element.
* 
* @returns { object } The output returned by this function is a `div` element
* representing a tip.
*/
    _createTipElement(content) {
      const tip = this._getTemplateFactory(content).toHtml();

      // TODO: remove this check in v6
      if (!tip) {
        return null;
      }
      tip.classList.remove(CLASS_NAME_FADE$2, CLASS_NAME_SHOW$2);
      // TODO: v6 the following can be achieved with CSS only
      tip.classList.add(`bs-${this.constructor.NAME}-auto`);
      const tipId = getUID(this.constructor.NAME).toString();
      tip.setAttribute('id', tipId);
      if (this._isAnimated()) {
        tip.classList.add(CLASS_NAME_FADE$2);
      }
      return tip;
    }
/**
* @description This function sets the new content of an object and updates the display
* status based on whether it is currently shown or not.
* 
* @param { string } content - The `content` input parameter is the new content that
* will be displayed by the component.
* 
* @returns { object } The function `setContent` takes a `content` parameter and sets
* the internal `_newContent` property to it. If the widget is already shown (checked
* with `_isShown()`), itdisposes of any existing popper and then shows itself again.
* 
* Output: Does not return anything.
*/
    setContent(content) {
      this._newContent = content;
      if (this._isShown()) {
        this._disposePopper();
        this.show();
      }
    }
/**
* @description The function `_getTemplateFactory` creates a `TemplateFactory` instance
* and either uses an existing one or creates a new one depending on whether one has
* been previously created for the current configuration.
* 
* @param { string } content - The `content` input parameter overrides the `content`
* property of the ` TemplateFactory` configuration object when creating a new instance
* of the factory.
* 
* @returns { object } The function `_getTemplateFactory` returns the `TemplateFactory`
* object. It creates a new instance of `TemplateFactory` if no existing factory is
* found for the current content and configuration.
*/
    _getTemplateFactory(content) {
      if (this._templateFactory) {
        this._templateFactory.changeContent(content);
      } else {
        this._templateFactory = new TemplateFactory({
          ...this._config,
          // the `content` var has to be after `this._config`
          // to override config.content in case of popover
          content,
          extraClass: this._resolvePossibleFunction(this._config.customClass)
        });
      }
      return this._templateFactory;
    }
/**
* @description This function returns an object with a single property `SELECTOR_TOOLTIP_INNER`
* set to the result of `this._getTitle()` method.
* 
* @returns { object } The function `_getContentForTemplate()` returns an object with
* one property: `SELECTOR_TOOLTIP_INNER`, set to the result of the function `_getTitle()`.
*/
    _getContentForTemplate() {
      return {
        [SELECTOR_TOOLTIP_INNER]: this._getTitle()
      };
    }
/**
* @description This function retrieves the title of an element either from a
* configuration object or an HTML attribute("data-bs-original-title") and returns it.
* 
* @returns { string } The output of `_getTitle()` is a string value that represents
* the title of an element. The function first checks if `this._config.title` exists
* and is a function then calls it to get its result (which may be a string or null),
* if not it tries to retrieve an attribute data-bs-original-title from the element
* and returns its string value or null if not found.
*/
    _getTitle() {
      return this._resolvePossibleFunction(this._config.title) || this._element.getAttribute('data-bs-original-title');
    }

    // Private
/**
* @description This function is a JavaScript function that returns an instance of a
* class (i.e., the constructor's returned value), given an event delegate target and
* configuration parameters for that class instance.
* 
* @param {  } event - The `event` input parameter is used to provide the target
* element that triggered the event.
* 
* @returns {  } Based on the code snippet provided:
* 
* The output of `undefined` is returned by this function because `this` is undefined
* within the function scope.
* 
* In brief: The function returns nothing (or undefined) as it cannot access the
* required `this` context due to its scope limitations.
*/
    _initializeOnDelegatedTarget(event) {
      return this.constructor.getOrCreateInstance(event.delegateTarget, this._getDelegateConfig());
    }
/**
* @description This function checks if the instance has animation or a fade tip class
* and returns a boolean value indicating whether the instance is animated or not.
* 
* @returns { boolean } The function `_isAnimated` returns a boolean value indicating
* whether the component is currently animated or not. It checks if the component's
* configuration has an animation set or if the tip element (if it exists) contains
* the class name `FADE`. If either of these conditions are true.
*/
    _isAnimated() {
      return this._config.animation || this.tip && this.tip.classList.contains(CLASS_NAME_FADE$2);
    }
/**
* @description This function checks whether the tip element (referred to by "this")
* has a class name containing the string CLASS_NAME_SHOW$2.
* 
* @returns { boolean } This function returns a boolean value indicating whether the
* tip element associated with this object has the class CLASS_NAME_SHOW.
*/
    _isShown() {
      return this.tip && this.tip.classList.contains(CLASS_NAME_SHOW$2);
    }
/**
* @description This function creates a Popper element based on the given `tip` element
* and attaches it to the `this._element` element using the `AttachmentMap` object.
* 
* @param {  } tip - The `tip` input parameter is the reference to the popover content
* element (e.g., a paragraph or list) that will be displayed when the user hovers
* over the anchor element.
* 
* @returns { Promise } The function `_createPopper(tip)` returns a new `Popper`
* instance created with the placement and attachment information derived from the
* config object and passed as arguments.
*/
    _createPopper(tip) {
      const placement = execute(this._config.placement, [this, tip, this._element]);
      const attachment = AttachmentMap[placement.toUpperCase()];
      return createPopper(this._element, tip, this._getPopperConfig(attachment));
    }
/**
* @description This function is named `_getOffset`, and it returns an array of numbers
* representing the offset (position) of an element relative to its parent.
* 
* @returns { array } The function `_getOffset` returns an array of numbers. If the
* `offset` property passed to the function is a string containing multiple values
* separated by commas and digits (e.g., "top-20px"), it will return an array of these
* values parsed as integers using `Number.parseInt(value)`.
* 
* If `offset` is a function that takes two arguments (popperData and referenceElement),
* the function will call that function with the current popper data and the reference
* element as its arguments and return the result of calling the function on those parameters.
*/
    _getOffset() {
      const {
        offset
      } = this._config;
      if (typeof offset === 'string') {
        return offset.split(',').map(value => Number.parseInt(value, 10));
      }
      if (typeof offset === 'function') {
        return popperData => offset(popperData, this._element);
      }
      return offset;
    }
/**
* @description This function is a prototype property named `_resolvePossibleFunction`
* and it resolves a possible function by executing it with the `execute()` function
* and passing it `arg` as an argument and `[this._element]` as additional arguments.
* 
* @param { any } arg - The `arg` input parameter is passed to the `execute` function
* as its second argument.
* 
* @returns { any } The given function is:
* ```js
* _resolvePossibleFunction(arg) {
*   return execute(arg,[this._element]);
* }
* ```
* The output of this function is:
* 
* 	- `execute(arg,[this._element])`
* 
* In other words., the function calls the `execute()` function with `arg` as its
* argument and an array containing only `this._element`.
*/
    _resolvePossibleFunction(arg) {
      return execute(arg, [this._element]);
    }
/**
* @description This function Returns the Popper.js configuration object for a given
* attachment value.
* 
* @param { string } attachment - The `attachment` input parameter is used to set the
* placement of the popper relative to its reference element.
* 
* @returns { object } The `_getPopperConfig` function takes an attachment as input
* and returns an object with the default BS Popper configuration and any additional
* modifications specified by the user's popper configuration.
*/
    _getPopperConfig(attachment) {
      const defaultBsPopperConfig = {
        placement: attachment,
        modifiers: [{
          name: 'flip',
          options: {
            fallbackPlacements: this._config.fallbackPlacements
          }
        }, {
          name: 'offset',
          options: {
            offset: this._getOffset()
          }
        }, {
          name: 'preventOverflow',
          options: {
            boundary: this._config.boundary
          }
        }, {
          name: 'arrow',
          options: {
            element: `.${this.constructor.NAME}-arrow`
          }
        }, {
          name: 'preSetPlacement',
          enabled: true,
          phase: 'beforeMain',
/**
* @description This function sets the `data-popper-placement` attribute on the tip
* element to the value of the `placement` property passed as a argument.
* 
* @param { object } data - In this context,
* 
* `data` is an event object providing access to relevant information passed from a
* parent element regarding this function's occurrence or completion
* 
* @returns {  } This function sets the `data-popper-placement` attribute on the tip
* element to the value of `data.state.placement`.
*/
          fn: data => {
            // Pre-set Popper's placement attribute in order to read the arrow sizes properly.
            // Otherwise, Popper mixes up the width and height dimensions since the initial arrow style is for top placement
            this._getTipElement().setAttribute('data-popper-placement', data.state.placement);
          }
        }]
      };
      return {
        ...defaultBsPopperConfig,
        ...execute(this._config.popperConfig, [defaultBsPopperConfig])
      };
    }
/**
* @description This function sets up event listeners for the buttons to toggle the
* modals. It splits the triggers config into individual triggers and sets event
* listeners for each trigger.
* 
* @returns { object } The output of `_setListeners()` is not defined because the
* function does not return anything.
*/
    _setListeners() {
      const triggers = this._config.trigger.split(' ');
      for (const trigger of triggers) {
        if (trigger === 'click') {
          EventHandler.on(this._element, this.constructor.eventName(EVENT_CLICK$1), this._config.selector, event => {
            const context = this._initializeOnDelegatedTarget(event);
            context.toggle();
          });
        } else if (trigger !== TRIGGER_MANUAL) {
          const eventIn = trigger === TRIGGER_HOVER ? this.constructor.eventName(EVENT_MOUSEENTER) : this.constructor.eventName(EVENT_FOCUSIN$1);
          const eventOut = trigger === TRIGGER_HOVER ? this.constructor.eventName(EVENT_MOUSELEAVE) : this.constructor.eventName(EVENT_FOCUSOUT$1);
          EventHandler.on(this._element, eventIn, this._config.selector, event => {
            const context = this._initializeOnDelegatedTarget(event);
            context._activeTrigger[event.type === 'focusin' ? TRIGGER_FOCUS : TRIGGER_HOVER] = true;
            context._enter();
          });
          EventHandler.on(this._element, eventOut, this._config.selector, event => {
            const context = this._initializeOnDelegatedTarget(event);
            context._activeTrigger[event.type === 'focusout' ? TRIGGER_FOCUS : TRIGGER_HOVER] = context._element.contains(event.relatedTarget);
            context._leave();
          });
        }
      }
      this._hideModalHandler = () => {
        if (this._element) {
          this.hide();
        }
      };
      EventHandler.on(this._element.closest(SELECTOR_MODAL), EVENT_MODAL_HIDE, this._hideModalHandler);
    }
/**
* @description The `fixTitle()` function sets the `aria-label` attribute of an element
* if the `title` attribute is present but there is no `textContent` or `aria-label`
* already set.
* 
* @returns { any } The `fixTitle` function takes an element and updates its title
* attribute and aria-label attribute. It removes the title attribute and sets the
* aria-label attribute if the element has no text content and no title attribute.
* Additionally , it sets the data-bs-original-title attribute which is not recommended
* for use and only kept for backward compatibility.
* The output of this function is not returned explicitly but rather affects the
* attributes of the passed element.
*/
    _fixTitle() {
      const title = this._element.getAttribute('title');
      if (!title) {
        return;
      }
      if (!this._element.getAttribute('aria-label') && !this._element.textContent.trim()) {
        this._element.setAttribute('aria-label', title);
      }
      this._element.setAttribute('data-bs-original-title', title); // DO NOT USE IT. Is only for backwards compatibility
      this._element.removeAttribute('title');
    }
/**
* @description This function implements a delay-based show/hide behavior for an element.
* 
* @returns {  } The output returned by the function is `undefined`.
* 
* In a nutshell:
* 
* 1/ If the element is already shown or hovered over (i.e., `_isShown() || _isHovered`),
* do nothing and return `undefined`.
* 2/ Set `_isHovered` to `true`.
* 3/ Call `setTimeout` to show the element after the configured delay (here's where
* the `this._config.delay.show` variable comes into play).
* 4/ Return `undefined`.
*/
    _enter() {
      if (this._isShown() || this._isHovered) {
        this._isHovered = true;
        return;
      }
      this._isHovered = true;
      this._setTimeout(() => {
        if (this._isHovered) {
          this.show();
        }
      }, this._config.delay.show);
    }
/**
* @description This function sets a timeout to hide the element after a certain delay
* if the element is not being hovered over.
* 
* @returns { any } The `leave()` function is an event handler for when the mouse
* leaves the element.
*/
    _leave() {
      if (this._isWithActiveTrigger()) {
        return;
      }
      this._isHovered = false;
      this._setTimeout(() => {
        if (!this._isHovered) {
          this.hide();
        }
      }, this._config.delay.hide);
    }
/**
* @description This function sets a timer to call the `handler` function after
* `timeout` milliseconds.
* 
* @param {  } handler - The `handler` input parameter is the function that will be
* executed after the specified `timeout` period.
* 
* @param { number } timeout - The `timeout` input parameter specifies the time (in
* milliseconds) before which the function provided as the first argument (`handler`)
* should be executed.
* 
* @returns { number } The function takes two arguments: `handler` and `timeout`.
*/
    _setTimeout(handler, timeout) {
      clearTimeout(this._timeout);
      this._timeout = setTimeout(handler, timeout);
    }
/**
* @description The function `_isWithActiveTrigger()` checks if any of the elements
* stored In `this._activeTrigger` are true.
* 
* @returns { boolean } This function is agetter for a property named "_isWithActiveTrigger"
* and it checks if any of the values inside the object "this._activeTrigger" are true.
* The output returned by this function is a boolean value: true if at least one value
* inside the _activeTrigger object is truthy (i.e., true), false otherwise.
*/
    _isWithActiveTrigger() {
      return Object.values(this._activeTrigger).includes(true);
    }
/**
* @description This function prepares a configuration object `config` for use within
* the component by:
* 
* 1/ Removing any disallowed attributes from the dataAttributes of the element.
* 2/ Merging the dataAttributes with any provided config object (if one is passed).
* 3/ Type-checking the resulting config object.
* 4/ Returning the prepared configuration object.
* 
* @param { object } config - The `config` input parameter is an optional object that
* is merged with the data attributes of the element and other configurations to
* create the final configuration object returned by the function.
* 
* @returns { object } The output returned by this function is the modified `config`
* object that has gone through several transformations:
* 
* 1/ Removed any "disallowed" attributes from the original `dataAttributes`.
* 2/ Merged the original `config` object with the processed `dataAttributes`, if it
* was provided.
* 3/ Recursively merged any nested objects.
* 4/ Performed type checking on the resulting config.
* 
* The output is a single configuration object that contains all allowed attributes
* from the original `dataAttributes` and any provided `config`.
*/
    _getConfig(config) {
      const dataAttributes = Manipulator.getDataAttributes(this._element);
      for (const dataAttribute of Object.keys(dataAttributes)) {
        if (DISALLOWED_ATTRIBUTES.has(dataAttribute)) {
          delete dataAttributes[dataAttribute];
        }
      }
      config = {
        ...dataAttributes,
        ...(typeof config === 'object' && config ? config : {})
      };
      config = this._mergeConfigObj(config);
      config = this._configAfterMerge(config);
      this._typeCheckConfig(config);
      return config;
    }
/**
* @description This function takes a configuration object `config` and modifies it
* by:
* 
* 1/ Setting the `container` property to `document.body` if it is not already defined
* or set to a valid Element.
* 2/ Converting any number properties (e.g.
* 
* @param { object } config - The `config` input parameter is a JSON-like object that
* contains various configuration options for the modal window.
* 
* @returns { object } The function takes a `config` object as input and modifies it
* to set default values for some of its properties. The output of the function is
* the modified `config` object.
* 
* The function updates the `container` property of the `config` object to set it to
* `document.body` if it was previously set to `false`, or the specified container
* element if a valid reference was provided.
* 
* It also checks if the `delay` and `title` properties are numeric and converts them
* to strings if necessary. Additionally. It checks if the `content` property is
* numeric and converts it to a string if necessary.
* 
* Finally. the function returns the modified `config` object.
*/
    _configAfterMerge(config) {
      config.container = config.container === false ? document.body : getElement(config.container);
      if (typeof config.delay === 'number') {
        config.delay = {
          show: config.delay,
          hide: config.delay
        };
      }
      if (typeof config.title === 'number') {
        config.title = config.title.toString();
      }
      if (typeof config.content === 'number') {
        config.content = config.content.toString();
      }
      return config;
    }
/**
* @description The function `_getDelegateConfig()`:
* 
* Creates an empty object `config`.
* loops through the properties of `this._config` that have values different from the
* constructor's defaults and sets `config[key]` to those values.
* sets `config.selector` to `false`, and `config.trigger` to `'manual'`.
* 
* @returns { object } The output returned by the function `_getDelegateConfig()` is
* an object that contains only those configuration keys that have values different
* from the default values defined by the constructor of the class. The object has
* the following properties:
* 
* 	- `selector`: false (indicating that no selector is specified)
* 	- `trigger`: 'manual' (indicating that the delegate will be triggered manually)
* 
* The function iterates through all configuration keys defined by the constructor
* and compares each key's value with the default value.
*/
    _getDelegateConfig() {
      const config = {};
      for (const [key, value] of Object.entries(this._config)) {
        if (this.constructor.Default[key] !== value) {
          config[key] = value;
        }
      }
      config.selector = false;
      config.trigger = 'manual';

      // In the future can be replaced with:
      // const keysWithDifferentValues = Object.entries(this._config).filter(entry => this.constructor.Default[entry[0]] !== this._config[entry[0]])
      // `Object.fromEntries(keysWithDifferentValues)`
      return config;
    }
/**
* @description This function disposese the popper and tip elements created by the
* popup component.
* 
* @returns {  } The output of the function is void.
*/
    _disposePopper() {
      if (this._popper) {
        this._popper.destroy();
        this._popper = null;
      }
      if (this.tip) {
        this.tip.remove();
        this.tip = null;
      }
    }

    // Static
/**
* @description This function is a jQuery plugin called `Tooltip`, and it provides a
* static interface for interacting with the tooltip instance on an element.
* 
* @param { object } config - The `config` parameter is an object or a string that
* contains configuration options for the tooltip instance being created or called.
* It specifies various settings such as content display timings and animation effects.
* The `config` object can also have properties named using methods that can be invoked
* on the tooltip instance using their names as method calls. However not all of these
* property/method pairs are defined by default.
* 
* @returns {  } The function `jQueryInterface` returns `this` (the element to which
* the jQuery plugin is attached) after executing a callback function on each element.
* The callback function gets an instance of the `Tooltip` object and config object
* as parameters and performs the operation specified by the `config` parameter.
*/
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Tooltip.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * jQuery
   */

  defineJQueryPlugin(Tooltip);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap popover.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$3 = 'popover';
  const SELECTOR_TITLE = '.popover-header';
  const SELECTOR_CONTENT = '.popover-body';
  const Default$2 = {
    ...Tooltip.Default,
    content: '',
    offset: [0, 8],
    placement: 'right',
    template: '<div class="popover" role="tooltip">' + '<div class="popover-arrow"></div>' + '<h3 class="popover-header"></h3>' + '<div class="popover-body"></div>' + '</div>',
    trigger: 'click'
  };
  const DefaultType$2 = {
    ...Tooltip.DefaultType,
    content: '(null|string|element|function)'
  };

  /**
   * Class definition
   */

  class Popover extends Tooltip {
    // Getters
/**
* @description This function returns the value of the `Default$2` constant.
* 
* @returns {  } The output returned by the function is `Default$2`.
*/
    static get Default() {
      return Default$2;
    }
/**
* @description This function returns a constant value named `DefaultType$2`.
* 
* @returns { string } The function returns `DefaultType$2`.
*/
    static get DefaultType() {
      return DefaultType$2;
    }
/**
* @description This is a Getter function that returns the value of a property named
* `NAME` by referencing it through `$3`.
* 
* @returns { string } The function returns "undefined".
* 
* Here's why:
* 
* 1/ The function is defined with the `static` keyword which means it belongs to the
* class and not to an instance of the class.
* 2/ The function `getName()` calls `NAME$3`, which is a variable that is undefined.
* 3/ Therefore when the function `getName()` is called it returns "undefined" as
* there is no value defined for `NAME$3`.
*/
    static get NAME() {
      return NAME$3;
    }

    // Overrides
/**
* @description This function checks if the current widget has either a title or
* content set.
* 
* @returns { boolean } The output of this function is a boolean value indicating
* whether the `this` object has both a title and content. The function checks if
* either `this._getTitle()` or `this._getContent()` returns a value. If either of
* them returns a value (i.e., truthy), the function returns true.
*/
    _isWithContent() {
      return this._getTitle() || this._getContent();
    }

    // Private
/**
* @description This function returns an object with two properties: `Selector Title`
* and `Selector Content`, where the values are respectively the title and content
* of the current template.
* 
* @returns { object } The output returned by `_getContentForTemplate()` is an object
* with two properties: `SELECTOR_TITLE` and `SELECTOR_CONTENT`. The values of these
* properties are determined by calling `_getTitle()` and `_getContent()`, respectively.
*/
    _getContentForTemplate() {
      return {
        [SELECTOR_TITLE]: this._getTitle(),
        [SELECTOR_CONTENT]: this._getContent()
      };
    }
/**
* @description This function is resolving a possibly undefined value `this._config.content`
* and returning its resolved value.
* 
* @returns { string } The function `_getContent()` returns the resolved value of the
* `content` property of the object's config. If the property is a function then it
* is invoked and its return value is resolved. If the property is not a function
* then its value is returned as is.
* 
* In other words:
* 
* 	- If `this._config.content` is a function: The function is called and its return
* value is resolved (whatever it might be - a string or an object).
* 	- If `this._config.content` is not a function: The property's value is returned
* as is (i.e., the original value).
* 
* So the output returned by this function will depend on the value of `this._config.content`.
*/
    _getContent() {
      return this._resolvePossibleFunction(this._config.content);
    }

    // Static
/**
* @description This function is a JavaScript method called `jQueryInterface` that
* takes a configuration object as an argument.
* 
* @param { object } config - The `config` input parameter is an object that contains
* configuration options for the Popover instance.
* 
* @returns { object } This function is a JavaScript Object literal (literally written
* as a collection of key-value pairs).
*/
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Popover.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * jQuery
   */

  defineJQueryPlugin(Popover);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap scrollspy.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$2 = 'scrollspy';
  const DATA_KEY$2 = 'bs.scrollspy';
  const EVENT_KEY$2 = `.${DATA_KEY$2}`;
  const DATA_API_KEY = '.data-api';
  const EVENT_ACTIVATE = `activate${EVENT_KEY$2}`;
  const EVENT_CLICK = `click${EVENT_KEY$2}`;
  const EVENT_LOAD_DATA_API$1 = `load${EVENT_KEY$2}${DATA_API_KEY}`;
  const CLASS_NAME_DROPDOWN_ITEM = 'dropdown-item';
  const CLASS_NAME_ACTIVE$1 = 'active';
  const SELECTOR_DATA_SPY = '[data-bs-spy="scroll"]';
  const SELECTOR_TARGET_LINKS = '[href]';
  const SELECTOR_NAV_LIST_GROUP = '.nav, .list-group';
  const SELECTOR_NAV_LINKS = '.nav-link';
  const SELECTOR_NAV_ITEMS = '.nav-item';
  const SELECTOR_LIST_ITEMS = '.list-group-item';
  const SELECTOR_LINK_ITEMS = `${SELECTOR_NAV_LINKS}, ${SELECTOR_NAV_ITEMS} > ${SELECTOR_NAV_LINKS}, ${SELECTOR_LIST_ITEMS}`;
  const SELECTOR_DROPDOWN = '.dropdown';
  const SELECTOR_DROPDOWN_TOGGLE$1 = '.dropdown-toggle';
  const Default$1 = {
    offset: null,
    // TODO: v6 @deprecated, keep it for backwards compatibility reasons
    rootMargin: '0px 0px -25%',
    smoothScroll: false,
    target: null,
    threshold: [0.1, 0.5, 1]
  };
  const DefaultType$1 = {
    offset: '(number|null)',
    // TODO v6 @deprecated, keep it for backwards compatibility reasons
    rootMargin: 'string',
    smoothScroll: 'boolean',
    target: 'element',
    threshold: 'array'
  };

  /**
   * Class definition
   */

  class ScrollSpy extends BaseComponent {
/**
* @description This function is a constructor for an object that initializes a
* dropdown menu. It sets up member variables and properties related to the dropdown's
* display state and observer configuration.
* 
* @param {  } element - The `element` input parameter is the container element where
* the accordion is to be initialized.
* 
* @param { object } config - In this constructor function for a scrolling observer
* widget that scolls elements into view as you hover over links with infinite
* scrollability to be precise and a wide content area to fill lazily. The input
* paramerter `config` accepts configuration data and is an optional parameter.
* 
* @returns {  } The output returned by the function is an instance of a class that
* contains several properties and methods related to navigation and observing scroll
* behavior on a web page.
*/
    constructor(element, config) {
      super(element, config);

      // this._element is the observablesContainer and config.target the menu links wrapper
      this._targetLinks = new Map();
      this._observableSections = new Map();
      this._rootElement = getComputedStyle(this._element).overflowY === 'visible' ? null : this._element;
      this._activeTarget = null;
      this._observer = null;
      this._previousScrollData = {
        visibleEntryTop: 0,
        parentScrollTop: 0
      };
      this.refresh(); // initialize
    }

    // Getters
/**
* @description This function is a `getter` method that returns the value of the
* `Default` static property of the object.
* 
* @returns {  } The output returned by the function is `Default$1`.
*/
    static get Default() {
      return Default$1;
    }
/**
* @description This function is a `getter` method that returns the value of the
* `DefaultType` constant.
* 
* @returns { string } The function returns `DefaultType$1`.
*/
    static get DefaultType() {
      return DefaultType$1;
    }
/**
* @description This function is a getter method that returns the value of the `NAME$2`
* variable.
* 
* @returns { string } The output of this function is `NAME$2`.
* 
* The function has a `static` modifier which means that it belongs to the class and
* is not an instance method.
*/
    static get NAME() {
      return NAME$2;
    }

    // Public
/**
* @description This function refreshes the contents of a page by reinitializing
* targets and observables and updating the observer to monitor changes to the
* observable sections of the page.
* 
* @returns { any } The `refresh()` function returns nothing (i.e., it has no return
* statement).
*/
    refresh() {
      this._initializeTargetsAndObservables();
      this._maybeEnableSmoothScroll();
      if (this._observer) {
        this._observer.disconnect();
      } else {
        this._observer = this._getNewObserver();
      }
      for (const section of this._observableSections.values()) {
        this._observer.observe(section);
      }
    }
/**
* @description This function is a "dispose" method of an object.
* 
* @returns { any } The function `dispose()` does not return any value.
*/
    dispose() {
      this._observer.disconnect();
      super.dispose();
    }

    // Private
/**
* @description This function performs several tweaks and adjustments to the configuration
* object passed to it before returning the modified configuration. The key changes
* made are:
* 
* 1/ If `target` is not specified or is an element but not a document body element
* directly or indirectly under it will be replaced with `document.body`.
* 2/ Removes {target: 'ss-target'} as the property since it's now unnecessary due
* to point 1 above (i.e., all valid elements).
* 3/ Forwards compatibility reasons adjust the rootMargin setting based on offset
* or string threshold values.
* 
* @param { object } config - The `config` input parameter is the configuration object
* that is being modified by the function.
* 
* @returns { object } The function takes an object `config` as input and modifies
* some of its properties before returning it.
*/
    _configAfterMerge(config) {
      // TODO: on v6 target should be given explicitly & remove the {target: 'ss-target'} case
      config.target = getElement(config.target) || document.body;

      // TODO: v6 Only for backwards compatibility reasons. Use rootMargin only
      config.rootMargin = config.offset ? `${config.offset}px 0px -30%` : config.rootMargin;
      if (typeof config.threshold === 'string') {
        config.threshold = config.threshold.split(',').map(value => Number.parseFloat(value));
      }
      return config;
    }
/**
* @description This function enables smooth scrolling for links within a specified
* target element by registering an event listener that prevents default linking
* behavior and instead smoothly scrolls to the top of the visible portion of the
* observable section linked to.
* 
* @returns { any } The function `_maybeEnableSmoothScroll()` returns nothing (undefined)
* as it is a void function. Its purpose is to enable smooth scrolling for links with
* hashes within a specific section of the page.
*/
    _maybeEnableSmoothScroll() {
      if (!this._config.smoothScroll) {
        return;
      }

      // unregister any previous listeners
      EventHandler.off(this._config.target, EVENT_CLICK);
      EventHandler.on(this._config.target, EVENT_CLICK, SELECTOR_TARGET_LINKS, event => {
        const observableSection = this._observableSections.get(event.target.hash);
        if (observableSection) {
          event.preventDefault();
          const root = this._rootElement || window;
          const height = observableSection.offsetTop - this._element.offsetTop;
          if (root.scrollTo) {
            root.scrollTo({
              top: height,
              behavior: 'smooth'
            });
            return;
          }

          // Chrome 60 doesn't support `scrollTo`
          root.scrollTop = height;
        }
      });
    }
/**
* @description This function creates a new `IntersectionObserver` instance and returns
* it.
* 
* @returns {  } The `getNewObserver` function returns a new `IntersectionObserver`
* instance with the given options.
*/
    _getNewObserver() {
      const options = {
        root: this._rootElement,
        threshold: this._config.threshold,
        rootMargin: this._config.rootMargin
      };
      return new IntersectionObserver(entries => this._observerCallback(entries), options);
    }

    // The logic of selection
/**
* @description This function observes scrolling events on an element and identifies
* the nearest intersecting target element when scrolling.
* 
* @param { object } entries - The `entries` input parameter is an array of entry
* objects that contain information about the current intersections between the
* observer's viewport and the links on the page. It contains objects with properties
* like `target`, `offsetTop`, `intersectionRect`, etc.
* 
* @returns { array } This function takes an array of entry objects as input and
* returns nothing (void). It processes each entry and determines which one is currently
* visible and should be activated based on the current scroll position and offset heights.
*/
    _observerCallback(entries) {
/**
* @description The given function is a getter method that returns the Element object
* referenced by the `_targetLinks` dictionary with the given `entry.target.id` as
* its key.
* 
* @param { object } entry - The `entry` parameter is a dictionary-like object that
* contains information about a specific link being processed. It includes properties
* like `target`, `from`, and other attributes related to the link.
* 
* @returns {  } The function `targetElement` takes an `entry` object as its argument
* and returns the Element object corresponding to the target of the entry.
*/
      const targetElement = entry => this._targetLinks.get(`#${entry.target.id}`);
/**
* @description This function "activate" saves the top position of the current entry
* being clicked and processes the target element of that entry.
* 
* @param { object } entry - The `entry` parameter is a scroll event entry object
* that contains information about the scrolled element.
* 
* @returns { any } This function `activate` takes an `entry` parameter and returns
* nothing (i.e., `undefined`) because it is a void function.
*/
      const activate = entry => {
        this._previousScrollData.visibleEntryTop = entry.target.offsetTop;
        this._process(targetElement(entry));
      };
      const parentScrollTop = (this._rootElement || document.documentElement).scrollTop;
      const userScrollsDown = parentScrollTop >= this._previousScrollData.parentScrollTop;
      this._previousScrollData.parentScrollTop = parentScrollTop;
      for (const entry of entries) {
        if (!entry.isIntersecting) {
          this._activeTarget = null;
          this._clearActiveClass(targetElement(entry));
          continue;
        }
        const entryIsLowerThanPrevious = entry.target.offsetTop >= this._previousScrollData.visibleEntryTop;
        // if we are scrolling down, pick the bigger offsetTop
        if (userScrollsDown && entryIsLowerThanPrevious) {
          activate(entry);
          // if parent isn't scrolled, let's keep the first visible item, breaking the iteration
          if (!parentScrollTop) {
            return;
          }
          continue;
        }

        // if we are scrolling up, pick the smallest offsetTop
        if (!userScrollsDown && !entryIsLowerThanPrevious) {
          activate(entry);
        }
      }
    }
/**
* @description This function initializes two maps (`_targetLinks` and `_observableSections`)
* that will be used to keep track of the target links and the corresponding observable
* sections found on the page. It does this by selecting all target links using a CSS
* selector (not shown), filtering out any links that are disabled or without an ID
* hash property and then checking if each remaining link's hash matches a URL anchor
* on the page.
* 
* @returns { string } This function takes two arguments: _config (an object) and
* _element (a DOMElement). It returns two maps: _targetLinks (a Map of hashes to
* anchors) and _observableSections (a Map of hashes to observable sections). The
* function finds all links with the SELECTOR_TARGET_LINKS selector and ensures that
* the anchor has an ID and is not disabled.
*/
    _initializeTargetsAndObservables() {
      this._targetLinks = new Map();
      this._observableSections = new Map();
      const targetLinks = SelectorEngine.find(SELECTOR_TARGET_LINKS, this._config.target);
      for (const anchor of targetLinks) {
        // ensure that the anchor has an id and is not disabled
        if (!anchor.hash || isDisabled(anchor)) {
          continue;
        }
        const observableSection = SelectorEngine.findOne(decodeURI(anchor.hash), this._element);

        // ensure that the observableSection exists & is visible
        if (isVisible(observableSection)) {
          this._targetLinks.set(decodeURI(anchor.hash), anchor);
          this._observableSections.set(anchor.hash, observableSection);
        }
      }
    }
/**
* @description This function sets the currently active element and adds a CSS class
* to the active element and its parents.
* 
* @param {  } target - The `target` input parameter is the element that the active
* class should be switched to.
* 
* @returns { any } This function takes a `target` parameter and performs the following
* actions:
* 
* 1/ If the current active target is the same as the passed `target`, it does nothing.
* 2/ Clears any active class from the previous target.
* 3/ Sets the `target` element as the new active target.
* 4/ Adds a specific class (defined by `CLASS_NAME_ACTIVE`) to the `target` element.
* 5/ Triggers an `EVENT_ACTIVATE` event on the parent element of the `target`, passing
* `relatedTarget: target`.
* 
* Therefore the output returned by this function is undefined.
*/
    _process(target) {
      if (this._activeTarget === target) {
        return;
      }
      this._clearActiveClass(this._config.target);
      this._activeTarget = target;
      target.classList.add(CLASS_NAME_ACTIVE$1);
      this._activateParents(target);
      EventHandler.trigger(this._element, EVENT_ACTIVATE, {
        relatedTarget: target
      });
    }
/**
* @description This function Activates dropdown parents when a dropdown item is clicked.
* 
* @param { object } target - The `target` input parameter is the element that triggered
* the activation of its dropdown parents.
* 
* @returns { any } This function takes a target element as input and activates its
* dropdown parents by adding the `CLASS_NAME_ACTIVE` class to them. The output of
* the function is the activation of the dropdown parents of the given target element.
*/
    _activateParents(target) {
      // Activate dropdown parents
      if (target.classList.contains(CLASS_NAME_DROPDOWN_ITEM)) {
        SelectorEngine.findOne(SELECTOR_DROPDOWN_TOGGLE$1, target.closest(SELECTOR_DROPDOWN)).classList.add(CLASS_NAME_ACTIVE$1);
        return;
      }
      for (const listGroup of SelectorEngine.parents(target, SELECTOR_NAV_LIST_GROUP)) {
        // Set triggered links parents as active
        // With both <ul> and <nav> markup a parent is the previous sibling of any nav ancestor
        for (const item of SelectorEngine.prev(listGroup, SELECTOR_LINK_ITEMS)) {
          item.classList.add(CLASS_NAME_ACTIVE$1);
        }
      }
    }
/**
* @description This function removes the `CLASS_NAME_ACTIVE$1` class from all elements
* matching a specific selector within the parent element and its descendants.
* 
* @param {  } parent - The `parent` parameter is used to specify the parent element
* from which the active class should be removed.
* 
* @returns { any } The output returned by the `undefined` function is `void`. In
* other words. the function does not return any value or data; instead it modifies
* the class list of a parent element and its child nodes.
*/
    _clearActiveClass(parent) {
      parent.classList.remove(CLASS_NAME_ACTIVE$1);
      const activeNodes = SelectorEngine.find(`${SELECTOR_TARGET_LINKS}.${CLASS_NAME_ACTIVE$1}`, parent);
      for (const node of activeNodes) {
        node.classList.remove(CLASS_NAME_ACTIVE$1);
      }
    }

    // Static
/**
* @description This function is the `static jQueryInterface` method for the ScrollSpy
* widget. It takes a configuration object as an argument and iterates over each
* element that has been jQuery-ized (i.e., wrapped with the `$()` selector) within
* the page.
* 
* @param { object } config - The `config` parameter is an object that contains options
* and configurations for the ScrollSpy instance being created.
* 
* @returns { object } This function returns `undefined`.
*/
    static jQueryInterface(config) {
      return this.each(function () {
        const data = ScrollSpy.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(window, EVENT_LOAD_DATA_API$1, () => {
    for (const spy of SelectorEngine.find(SELECTOR_DATA_SPY)) {
      ScrollSpy.getOrCreateInstance(spy);
    }
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(ScrollSpy);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap tab.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$1 = 'tab';
  const DATA_KEY$1 = 'bs.tab';
  const EVENT_KEY$1 = `.${DATA_KEY$1}`;
  const EVENT_HIDE$1 = `hide${EVENT_KEY$1}`;
  const EVENT_HIDDEN$1 = `hidden${EVENT_KEY$1}`;
  const EVENT_SHOW$1 = `show${EVENT_KEY$1}`;
  const EVENT_SHOWN$1 = `shown${EVENT_KEY$1}`;
  const EVENT_CLICK_DATA_API = `click${EVENT_KEY$1}`;
  const EVENT_KEYDOWN = `keydown${EVENT_KEY$1}`;
  const EVENT_LOAD_DATA_API = `load${EVENT_KEY$1}`;
  const ARROW_LEFT_KEY = 'ArrowLeft';
  const ARROW_RIGHT_KEY = 'ArrowRight';
  const ARROW_UP_KEY = 'ArrowUp';
  const ARROW_DOWN_KEY = 'ArrowDown';
  const CLASS_NAME_ACTIVE = 'active';
  const CLASS_NAME_FADE$1 = 'fade';
  const CLASS_NAME_SHOW$1 = 'show';
  const CLASS_DROPDOWN = 'dropdown';
  const SELECTOR_DROPDOWN_TOGGLE = '.dropdown-toggle';
  const SELECTOR_DROPDOWN_MENU = '.dropdown-menu';
  const NOT_SELECTOR_DROPDOWN_TOGGLE = ':not(.dropdown-toggle)';
  const SELECTOR_TAB_PANEL = '.list-group, .nav, [role="tablist"]';
  const SELECTOR_OUTER = '.nav-item, .list-group-item';
  const SELECTOR_INNER = `.nav-link${NOT_SELECTOR_DROPDOWN_TOGGLE}, .list-group-item${NOT_SELECTOR_DROPDOWN_TOGGLE}, [role="tab"]${NOT_SELECTOR_DROPDOWN_TOGGLE}`;
  const SELECTOR_DATA_TOGGLE = '[data-bs-toggle="tab"], [data-bs-toggle="pill"], [data-bs-toggle="list"]'; // TODO: could only be `tab` in v6
  const SELECTOR_INNER_ELEM = `${SELECTOR_INNER}, ${SELECTOR_DATA_TOGGLE}`;
  const SELECTOR_DATA_TOGGLE_ACTIVE = `.${CLASS_NAME_ACTIVE}[data-bs-toggle="tab"], .${CLASS_NAME_ACTIVE}[data-bs-toggle="pill"], .${CLASS_NAME_ACTIVE}[data-bs-toggle="list"]`;

  /**
   * Class definition
   */

  class Tab extends BaseComponent {
/**
* @description This function is a constructor for an object that sets up the initial
* state of an element that has a tab panel.
* 
* @param {  } element - The `element` input parameter is the HTML element that is
* being converted into a widget.
* 
* @returns {  } This function is a constructor for an object that takes an HTML
* element as an argument and sets up the object's properties and event listeners
* based on that element. The output returned by this function is not explicitly
* stated but can be inferred to be the newly created object instance with properties
* and event listeners set up.
*/
    constructor(element) {
      super(element);
      this._parent = this._element.closest(SELECTOR_TAB_PANEL);
      if (!this._parent) {
        return;
        // TODO: should throw exception in v6
        // throw new TypeError(`${element.outerHTML} has not a valid parent ${SELECTOR_INNER_ELEM}`)
      }

      // Set up initial aria attributes
      this._setInitialAttributes(this._parent, this._getChildren());
      EventHandler.on(this._element, EVENT_KEYDOWN, event => this._keydown(event));
    }

    // Getters
/**
* @description This function is a getter method that returns the value of a static
* variable called `NAME`.
* 
* @returns { string } The output returned by this function is `NAME$1`.
*/
    static get NAME() {
      return NAME$1;
    }

    // Public
/**
* @description This function shows the element specified by `this._element`, and
* deactivates any previously active element on the same parent.
* 
* @returns {  } The output returned by the `show()` function is not specified. The
* function performs various actions such as searching for an active tab on the same
* parent element to deactivate it and then activating the passed element.
*/
    show() {
      // Shows this elem and deactivate the active sibling if exists
      const innerElem = this._element;
      if (this._elemIsActive(innerElem)) {
        return;
      }

      // Search for active tab on same parent to deactivate it
      const active = this._getActiveElem();
      const hideEvent = active ? EventHandler.trigger(active, EVENT_HIDE$1, {
        relatedTarget: innerElem
      }) : null;
      const showEvent = EventHandler.trigger(innerElem, EVENT_SHOW$1, {
        relatedTarget: active
      });
      if (showEvent.defaultPrevented || hideEvent && hideEvent.defaultPrevented) {
        return;
      }
      this._deactivate(active, innerElem);
      this._activate(innerElem, active);
    }

    // Private
/**
* @description This function `_activate` is called when a tab link is clicked. It
* adds the 'active' class to the current tab and show its corresponding section by
* searching and activating/showing the proper section.
* 
* @param {  } element - The `element` input parameter is the HTML element that was
* clicked or touched to activate the tabbable element.
* 
* @param {  } relatedElem - The `relatedElem` input parameter passed to `_activate()`
* is used as the "related target" for the `EVENT_SHOWN$1` event that's triggered
* when the element is shown.
* 
* @returns {  } The output returned by the function `_activate` is not explicitly
* stated since it does not return anything explicitly.
*/
    _activate(element, relatedElem) {
      if (!element) {
        return;
      }
      element.classList.add(CLASS_NAME_ACTIVE);
      this._activate(SelectorEngine.getElementFromSelector(element)); // Search and activate/show the proper section

/**
* @description This function completes (or "shows") an element with a given `role`
* attribute that is not a tab. If the element has no tabindex and the role is a tab
* and shows it.
* 
* @returns {  } This function takes an element as an argument and adds a show class
* to it if the element has a role other than "tab". If the element has tabindex and
* is shown via an ARIA attribute of selected true and the event shown is triggered.
*/
      const complete = () => {
        if (element.getAttribute('role') !== 'tab') {
          element.classList.add(CLASS_NAME_SHOW$1);
          return;
        }
        element.removeAttribute('tabindex');
        element.setAttribute('aria-selected', true);
        this._toggleDropDown(element, true);
        EventHandler.trigger(element, EVENT_SHOWN$1, {
          relatedTarget: relatedElem
        });
      };
      this._queueCallback(complete, element, element.classList.contains(CLASS_NAME_FADE$1));
    }
/**
* @description This function is called `_deactivate` and it deactivates an HTML
* element (typically a tab).
* 
* @param {  } element - The `element` input parameter is passed as a reference to
* the DOM element for which the method should be executed.
* 
* @param { object } relatedElem - The `relatedElem` input parameter is used to specify
* the element that triggered the deactivation of the current element.
* 
* @returns {  } The output returned by the function `_deactivate` is not specified
* as it is a void function meaning that it does not return any value or output.
*/
    _deactivate(element, relatedElem) {
      if (!element) {
        return;
      }
      element.classList.remove(CLASS_NAME_ACTIVE);
      element.blur();
      this._deactivate(SelectorEngine.getElementFromSelector(element)); // Search and deactivate the shown section too

/**
* @description This function undoes the effect of a previously called `show` function.
* 
* @returns {  } This function takes an `event` object as input and returns nothing
* (i.e., `undefined`). It has three main lines of logic:
* 
* 1/ It checks if the event target element has a certain attribute ("role" with value
* "tab"). If it does not have this attribute or its value is not "tab", the function
* will exit early without making any changes to the element.
* 2/ If the element does have the "tab" role attribute and the function did not exit
* early above (i.e., if `element.getAttribute('role') === 'tab'`), the function will
* set two attributes on the event target element: `aria-selected` to `false` and
* `tabindex` to `-1`.
* 3/ It will also call a private method called `_toggleDropDown()` with the event
* target element and `false` as arguments.
* 
* The function also triggers an event named `EVENT_HIDDEN$1` on the event target
* element with the `relatedTarget` set to the related element passed as `relatedElem`.
*/
      const complete = () => {
        if (element.getAttribute('role') !== 'tab') {
          element.classList.remove(CLASS_NAME_SHOW$1);
          return;
        }
        element.setAttribute('aria-selected', false);
        element.setAttribute('tabindex', '-1');
        this._toggleDropDown(element, false);
        EventHandler.trigger(element, EVENT_HIDDEN$1, {
          relatedTarget: relatedElem
        });
      };
      this._queueCallback(complete, element, element.classList.contains(CLASS_NAME_FADE$1));
    }
/**
* @description This function listens for arrow key presses on an element and navigates
* to the next focused element within the same group of elements. If a disabled element
* is found during navigation , the navigation skips over it and prevents scroll
* behavior .
* 
* @param {  } event - The `event` parameter is an object that contains information
* about the keyboard event that triggered the function call.
* 
* @returns {  } This function takes an `event` object as input and returns nothing
* (it has a void return type). The function listens for keyboard events on the
* elements being managed by the `TabManager` instance. When an event is triggered
* (e.g., an arrow key press), the function checks if the event key is one of the
* arrow keys (up/down/left/right), and if it is not one of those keys then it does
* nothing (returns).
*/
    _keydown(event) {
      if (![ARROW_LEFT_KEY, ARROW_RIGHT_KEY, ARROW_UP_KEY, ARROW_DOWN_KEY].includes(event.key)) {
        return;
      }
      event.stopPropagation(); // stopPropagation/preventDefault both added to support up/down keys without scrolling the page
      event.preventDefault();
      const isNext = [ARROW_RIGHT_KEY, ARROW_DOWN_KEY].includes(event.key);
      const nextActiveElement = getNextActiveElement(this._getChildren().filter(element => !isDisabled(element)), event.target, isNext, true);
      if (nextActiveElement) {
        nextActiveElement.focus({
          preventScroll: true
        });
        Tab.getOrCreateInstance(nextActiveElement).show();
      }
    }
/**
* @description This function `_getChildren()` returns a collection of inner elements
* (using `SelectorEngine.find`) based on the `SELECTOR_INNER_ELEM` selector and the
* current element's parent element.
* 
* @returns { object } This function returns a collection of inner HTML elements using
* the `SelectorEngine` instance method `find()`.
*/
    _getChildren() {
      // collection of inner elements
      return SelectorEngine.find(SELECTOR_INNER_ELEM, this._parent);
    }
/**
* @description This function `_getActiveElem()` returns the currently active element
* within a collection of child elements (generated by `this._getChildren()`) or
* `null` if no element is active.
* 
* @returns { object } The ` _getActiveElem()` function returns either the currently
* active element (which is a child of the parent element) or `null` if no element
* is currently active.
*/
    _getActiveElem() {
      return this._getChildren().find(child => this._elemIsActive(child)) || null;
    }
/**
* @description This function sets the initial attributes for a set of children
* elements. It first sets the 'role' attribute to 'tablist' on the parent element
* if it doesn't already exist.
* 
* @param {  } parent - The `parent` input parameter is used to set the initial
* attributes on the parent element.
* 
* @param { array } children - The `children` input parameter is an array of child
* elements that should be processed by the `setInitialAttributes()` method.
* 
* @returns { any } This function takes two parameters `parent` and `children`, and
* it sets initial attributes on the `parent` element and its child elements.
*/
    _setInitialAttributes(parent, children) {
      this._setAttributeIfNotExists(parent, 'role', 'tablist');
      for (const child of children) {
        this._setInitialAttributesOnChild(child);
      }
    }
/**
* @description This function sets initial attributes on a child element (specifically
* aria-selected and tabindex) based on the state of its outer element and related panel.
* 
* @param {  } child - The `child` input parameter is a reference to an element that
* has been passed as a argument to the function.
* 
* @returns {  } This function sets various attributes on a child element `child`,
* and the output is that the attribute `aria-selected` is set to `true` or `false`,
* depending on the active state of the child element. Additionally `tabindex` is set
* to `-1` if the child element is not active.
*/
    _setInitialAttributesOnChild(child) {
      child = this._getInnerElement(child);
      const isActive = this._elemIsActive(child);
      const outerElem = this._getOuterElement(child);
      child.setAttribute('aria-selected', isActive);
      if (outerElem !== child) {
        this._setAttributeIfNotExists(outerElem, 'role', 'presentation');
      }
      if (!isActive) {
        child.setAttribute('tabindex', '-1');
      }
      this._setAttributeIfNotExists(child, 'role', 'tab');

      // set attributes to the related panel too
      this._setInitialAttributesOnTargetPanel(child);
    }
/**
* @description This function sets initial attributes on a target panel based on the
* properties of a child element passed as an argument.
* 
* @param { object } child - The `child` input parameter is a selector that identifies
* the element for which the function sets initial attributes.
* 
* @returns {  } Based on the code provided:
* 
* The `setInitialAttributesOnTargetPanel` function takes a `child` argument and
* returns nothing (undefined) because there is no statement that explicitly returns
* a value. The function modifies the attributes of an HTML element using the
* `querySelector` method and the `setAttributeIfNotExists` method.
*/
    _setInitialAttributesOnTargetPanel(child) {
      const target = SelectorEngine.getElementFromSelector(child);
      if (!target) {
        return;
      }
      this._setAttributeIfNotExists(target, 'role', 'tabpanel');
      if (child.id) {
        this._setAttributeIfNotExists(target, 'aria-labelledby', `${child.id}`);
      }
    }
/**
* @description This function _toggleDropDown(element、open) enables or disables the
* dropdown element's show/hide toggle based on a class applied to its outer element.
* 
* @param {  } element - The `element` input parameter is the dropdown element that
* triggered the toggle event.
* 
* @param { boolean } open - The `open` input parameter is a boolean value that
* determines whether to toggle the "active" class on the dropdown trigger element
* (select element) or not.
* 
* @returns {  } This function takes an element and a boolean `open` parameter. It
* adds or removes the `CLASS_NAME_ACTIVE` and `CLASS_NAME_SHOW$1` classes from the
* element and its surrounding `outerElem`, and sets the `aria-expanded` attribute
* of the outer element to `open`. The output is not explicitly returned by the function.
*/
    _toggleDropDown(element, open) {
      const outerElem = this._getOuterElement(element);
      if (!outerElem.classList.contains(CLASS_DROPDOWN)) {
        return;
      }
/**
* @description This function toggle() adds or removes a class name (passed as a
* string argument) to an element matched by the selector (also passed as a string
* argument) inside the outerElem element.
* 
* @param { string } selector - In this function `toggle`, the `selector` parameter
* is a string that represents the selector (a CSS selector) used to find an element
* to toggle the class on.
* 
* @param { string } className - The `className` input parameter is used to specify
* the class name that should be toggled on or off when the element is found.
* 
* @returns {  } The `toggle` function takes two arguments: a CSS selector and a class
* name. It uses `SelectorEngine.findOne` to find an element matching the selector
* and then toggles the class name on that element if it exists.
* 
* The output of the function is not explicitly returned; instead the function modifies
* the class list of the element found by the selector.
*/
      const toggle = (selector, className) => {
        const element = SelectorEngine.findOne(selector, outerElem);
        if (element) {
          element.classList.toggle(className, open);
        }
      };
      toggle(SELECTOR_DROPDOWN_TOGGLE, CLASS_NAME_ACTIVE);
      toggle(SELECTOR_DROPDOWN_MENU, CLASS_NAME_SHOW$1);
      outerElem.setAttribute('aria-expanded', open);
    }
/**
* @description This function sets an attribute on an HTML element if it doesn't
* already have that attribute.
* 
* @param { any } element - The `element` parameter is passed as a DOM element object
* to be modified by the function.
* 
* @param { string } attribute - In the function `_setAttributeIfNotExists`, the
* `attribute` parameter is used to specify the name of the attribute to be set on
* the element.
* 
* @param { string } value - The `value` input parameter sets the value for the
* specified attribute when it doesn't exist on the element.
* 
* @returns {  } The output returned by this function is void. The function does not
* return any value.
*/
    _setAttributeIfNotExists(element, attribute, value) {
      if (!element.hasAttribute(attribute)) {
        element.setAttribute(attribute, value);
      }
    }
/**
* @description This function checks if an HTML element has the class name "active"
* using the `classList` property and returns a boolean value indicating whether the
* element is active or not.
* 
* @param {  } elem - The `elem` input parameter is a HTML element that the function
* will check if it has the `CLASS_NAME_ACTIVE` class.
* 
* @returns { boolean } The function `_elemIsActive` takes an element `elem` as input
* and returns a boolean value indicating whether the element has the class `CLASS_NAME_ACTIVE`.
*/
    _elemIsActive(elem) {
      return elem.classList.contains(CLASS_NAME_ACTIVE);
    }

    // Try to get the inner element (usually the .nav-link)
/**
* @description The given function `_getInnerElement(elem)` is attempting to find an
* inner element of an HTML document.
* 
* @param {  } elem - The `elem` input parameter is the element being searched for
* an inner element. It is used to determine if the outer element matches the specified
* selector and return itself if it does.
* 
* @returns { object } The output returned by this function is either the element
* `elem` itself if it matches the selector `SELECTOR_INNER_ELEM`, or
* `SelectroEngine.findOne(SELECTOR_INNER_ELEM`, elem)` if it doesn't match.
*/
    _getInnerElement(elem) {
      return elem.matches(SELECTOR_INNER_ELEM) ? elem : SelectorEngine.findOne(SELECTOR_INNER_ELEM, elem);
    }

    // Try to get the outer element (usually the .nav-item)
/**
* @description The function `_getOuterElement(elem)` returns the closest outer element
* to `elem`, either the parent element that matches the selector `SELECTOR_OUTER`
* or `elem` itself if no such parent is found.
* 
* @param {  } elem - The `elem` parameter is the element to start searching for an
* outer element from.
* 
* @returns { object } The `return` statement of this function is equivalent to `return
* elem || elem.closest(SELECTOR_OUTER)`. It returns `elem` if it matches the
* `SELECTOR_OUTER` selector or if it does not have a closest match. If both conditions
* are met then `NULL` will be returned since an `Undefined` result was passed into
* the function and no other value is returned by either side of the OR operation
* (the return statements of each side is not explicitly listed).
*/
    _getOuterElement(elem) {
      return elem.closest(SELECTOR_OUTER) || elem;
    }

    // Static
/**
* @description This function is a jQuery-style static interface for tab objects. It
* takes an configuration object and iterates through each tab element on the page.
* If the configuration object contains a method name that doesn't exist or starts
* with an underscore or is 'constructor', it throws a TypeError.
* 
* @param { object } config - In the provided function `static jQueryInterface(config)`,
* the `config` parameter is an object or a string that contains the method name to
* be called on the `data` instance.
* 
* @returns { object } The function takes an `config` object and calls `each` method
* on the `Tab` prototype to iterate over all tabs. For each tab it checks if the
* config property exists and if it does not exist or starts with underscore or is
* equal to 'constructor', it throws a TypeError. If the config property exists and
* is a valid method name it gets called on the tab object.
*/
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Tab.getOrCreateInstance(this);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API, SELECTOR_DATA_TOGGLE, function (event) {
    if (['A', 'AREA'].includes(this.tagName)) {
      event.preventDefault();
    }
    if (isDisabled(this)) {
      return;
    }
    Tab.getOrCreateInstance(this).show();
  });

  /**
   * Initialize on focus
   */
  EventHandler.on(window, EVENT_LOAD_DATA_API, () => {
    for (const element of SelectorEngine.find(SELECTOR_DATA_TOGGLE_ACTIVE)) {
      Tab.getOrCreateInstance(element);
    }
  });
  /**
   * jQuery
   */

  defineJQueryPlugin(Tab);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap toast.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME = 'toast';
  const DATA_KEY = 'bs.toast';
  const EVENT_KEY = `.${DATA_KEY}`;
  const EVENT_MOUSEOVER = `mouseover${EVENT_KEY}`;
  const EVENT_MOUSEOUT = `mouseout${EVENT_KEY}`;
  const EVENT_FOCUSIN = `focusin${EVENT_KEY}`;
  const EVENT_FOCUSOUT = `focusout${EVENT_KEY}`;
  const EVENT_HIDE = `hide${EVENT_KEY}`;
  const EVENT_HIDDEN = `hidden${EVENT_KEY}`;
  const EVENT_SHOW = `show${EVENT_KEY}`;
  const EVENT_SHOWN = `shown${EVENT_KEY}`;
  const CLASS_NAME_FADE = 'fade';
  const CLASS_NAME_HIDE = 'hide'; // @deprecated - kept here only for backwards compatibility
  const CLASS_NAME_SHOW = 'show';
  const CLASS_NAME_SHOWING = 'showing';
  const DefaultType = {
    animation: 'boolean',
    autohide: 'boolean',
    delay: 'number'
  };
  const Default = {
    animation: true,
    autohide: true,
    delay: 5000
  };

  /**
   * Class definition
   */

  class Toast extends BaseComponent {
/**
* @description This function is a constructor for an object that sets up the listeners
* for mouse and keyboard interactions on an HTML element.
* 
* @param {  } element - The `element` parameter is the DOM element to which the
* widget will be attached.
* 
* @param { object } config - The `config` input parameter is used to pass configuration
* options to the constructor. In this case specifically it would contain things like
* mouse and keyboard interaction settings as indicated by the following lines.
* 
* @returns {  } The output of this function is an instance of the class created with
* the element and configuration parameters. This is done by calling the `super()`
* method to construct the parent object (in this case `google-polyfills.Object`).
* The instance also has several properties initialized to false: `_timeout`,
* `_hasMouseInteraction`, and `_hasKeyboardInteraction`.
*/
    constructor(element, config) {
      super(element, config);
      this._timeout = null;
      this._hasMouseInteraction = false;
      this._hasKeyboardInteraction = false;
      this._setListeners();
    }

    // Getters
/**
* @description This function simply returns the value of the `Default` constant.
* 
* @returns {  } The function returns `Default`.
*/
    static get Default() {
      return Default;
    }
/**
* @description This function returns the value of the "DefaultType" constant.
* 
* @returns {  } The output returned by this function is `DefaultType`.
*/
    static get DefaultType() {
      return DefaultType;
    }
/**
* @description This function returns the value of the `NAME` variable.
* 
* @returns {  } The function `NAME` is undefined and attempting to call it returns
* `undefined`.
*/
    static get NAME() {
      return NAME;
    }

    // Public
/**
* @description This function implements the show animation for a UI component.
* 
* @returns {  } The output returned by this function is the `EventHandler.trigger`
* event object.
*/
    show() {
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW);
      if (showEvent.defaultPrevented) {
        return;
      }
      this._clearTimeout();
      if (this._config.animation) {
        this._element.classList.add(CLASS_NAME_FADE);
      }
/**
* @description This function completes the hiding process of an element. It removes
* the "showing" class and triggers an event to indicate that the element has been shown.
* 
* @returns {  } The function `complete` takes no arguments and has a blank definition
* (`() => {}`).
*/
      const complete = () => {
        this._element.classList.remove(CLASS_NAME_SHOWING);
        EventHandler.trigger(this._element, EVENT_SHOWN);
        this._maybeScheduleHide();
      };
      this._element.classList.remove(CLASS_NAME_HIDE); // @deprecated
      reflow(this._element);
      this._element.classList.add(CLASS_NAME_SHOW, CLASS_NAME_SHOWING);
      this._queueCallback(complete, this._element, this._config.animation);
    }
/**
* @description The given function is a implementation of the `hide()` method for an
* object that has an element and some configuration options.
* 
* @returns { any } The `hide()` function returns nothing (void).
*/
    hide() {
      if (!this.isShown()) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE);
      if (hideEvent.defaultPrevented) {
        return;
      }
/**
* @description This function completes (or hides) the widget. It removes the
* CLASS_NAME_SHOWING and CLASS_NAME_SHOW classes from the element and adds the
* CLASS_NAME_HIDE class.
* 
* @returns {  } This function does several things:
* 
* 1/ It adds a class name to the element using `classList.add()`.
* 2/ It removes two class names from the element using `classList.remove()`.
* 3/ It triggers an event on the element using `EventHandler.trigger()`.
* 
* The output of this function is not explicitly returned.
*/
      const complete = () => {
        this._element.classList.add(CLASS_NAME_HIDE); // @deprecated
        this._element.classList.remove(CLASS_NAME_SHOWING, CLASS_NAME_SHOW);
        EventHandler.trigger(this._element, EVENT_HIDDEN);
      };
      this._element.classList.add(CLASS_NAME_SHOWING);
      this._queueCallback(complete, this._element, this._config.animation);
    }
/**
* @description This function is the "dispose" method of an object.
* 
* @returns { any } The output of the dispose() function is:
* 
* 	- Removing the CLASS_NAME_SHOW class from the element if it is shown.
* 	- Clearing any timeouts set by the widget.
* 	- Calling the super.dispose() method to free any additional resources allocated
* by the widget's parent class.
*/
    dispose() {
      this._clearTimeout();
      if (this.isShown()) {
        this._element.classList.remove(CLASS_NAME_SHOW);
      }
      super.dispose();
    }
/**
* @description The function `isShown()` checks if the element has the class name
* `CLASS_NAME_SHOW` or not.
* 
* @returns { boolean } The output returned by the `isShown()` function is a Boolean
* value indicating whether the element has the class `CLASS_NAME_SHOW` or not.
*/
    isShown() {
      return this._element.classList.contains(CLASS_NAME_SHOW);
    }

    // Private

/**
* @description This function schedules the hide method to be called after a delay
* (config.delay) if there is no mouse or keyboard interaction.
* 
* @returns {  } The `maybeScheduleHide` function returns nothing (i.e., it is a void
* function).
*/
    _maybeScheduleHide() {
      if (!this._config.autohide) {
        return;
      }
      if (this._hasMouseInteraction || this._hasKeyboardInteraction) {
        return;
      }
      this._timeout = setTimeout(() => {
        this.hide();
      }, this._config.delay);
    }
/**
* @description This function handles mouse and keyboard interactions for an element.
* It sets a flag for whether the element is currently being interacted with using
* `mouseover`, `mouseout`, or `focusin`, `focusout` events.
* 
* @param {  } event - The `event` parameter is passed into the function as an object
* that contains information about the user interaction that triggered the function's
* execution.
* 
* @param { boolean } isInteracting - The `isInteracting` input parameter indicates
* whether the user is currently interacting with the element.
* 
* @returns { object } This function takes two parameters: `event` and `isInteracting`.
*/
    _onInteraction(event, isInteracting) {
      switch (event.type) {
        case 'mouseover':
        case 'mouseout':
          {
            this._hasMouseInteraction = isInteracting;
            break;
          }
        case 'focusin':
        case 'focusout':
          {
            this._hasKeyboardInteraction = isInteracting;
            break;
          }
      }
      if (isInteracting) {
        this._clearTimeout();
        return;
      }
      const nextElement = event.relatedTarget;
      if (this._element === nextElement || this._element.contains(nextElement)) {
        return;
      }
      this._maybeScheduleHide();
    }
/**
* @description This function sets up event listeners on an element for mouseover and
* out events as well as focus-in and focus-out events.
* 
* @returns { any } This function sets event listeners for various events (`EVENT_MOUSEOVER`,
* `EVENT_MOUSEOUT`, `EVENT_FOCUSIN`, and `EVENT_FOCUSOUT) on an element represented
* by `_element`.
*/
    _setListeners() {
      EventHandler.on(this._element, EVENT_MOUSEOVER, event => this._onInteraction(event, true));
      EventHandler.on(this._element, EVENT_MOUSEOUT, event => this._onInteraction(event, false));
      EventHandler.on(this._element, EVENT_FOCUSIN, event => this._onInteraction(event, true));
      EventHandler.on(this._element, EVENT_FOCUSOUT, event => this._onInteraction(event, false));
    }
/**
* @description The given function is a method of an object that clears the `timeout`
* property by setting it to `null`.
* 
* @returns { any } The output returned by the function is `undefined`.
*/
    _clearTimeout() {
      clearTimeout(this._timeout);
      this._timeout = null;
    }

    // Static
/**
* @description This function is a static jQuery Interface (or jQuery plugin) that
* takes a config object as an argument and performs actions on the elements that are
* matched by the jQuery selection.
* 
* @param { object } config - The `config` parameter is an object or string that
* provides options for customizing the toast's appearance and behavior.
* 
* @returns { object } This function returns `this`.
*/
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Toast.getOrCreateInstance(this, config);
        if (typeof config === 'string') {
          if (typeof data[config] === 'undefined') {
            throw new TypeError(`No method named "${config}"`);
          }
          data[config](this);
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  enableDismissTrigger(Toast);

  /**
   * jQuery
   */

  defineJQueryPlugin(Toast);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap index.umd.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const index_umd = {
    Alert,
    Button,
    Carousel,
    Collapse,
    Dropdown,
    Modal,
    Offcanvas,
    Popover,
    ScrollSpy,
    Tab,
    Toast,
    Tooltip
  };

  return index_umd;

}));
//# sourceMappingURL=bootstrap.bundle.js.map
