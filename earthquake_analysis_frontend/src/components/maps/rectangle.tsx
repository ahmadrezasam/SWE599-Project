import {
  forwardRef,
  useContext,
  useEffect,
  useImperativeHandle,
  useMemo,
  useRef,
} from "react";

import { GoogleMapsContext, useMapsLibrary } from "@vis.gl/react-google-maps";

import type { Ref } from "react";

type RectangleEventProps = {
  onClick?: (e: google.maps.MapMouseEvent) => void;
  onDrag?: (e: google.maps.MapMouseEvent) => void;
  onDragStart?: (e: google.maps.MapMouseEvent) => void;
  onDragEnd?: (e: google.maps.MapMouseEvent) => void;
  onMouseOver?: (e: google.maps.MapMouseEvent) => void;
  onMouseOut?: (e: google.maps.MapMouseEvent) => void;
  onBoundsChanged?: (newBounds: google.maps.LatLngBoundsLiteral) => void;
};

type RectangleCustomProps = {
  /**
   * Bounds of the rectangle
   */
  bounds: google.maps.LatLngBoundsLiteral;
};

export type RectangleProps = google.maps.RectangleOptions &
  RectangleEventProps &
  RectangleCustomProps;

export type RectangleRef = Ref<google.maps.Rectangle | null>;

function useRectangle(props: RectangleProps) {
  const {
    onClick,
    onDrag,
    onDragStart,
    onDragEnd,
    onMouseOver,
    onMouseOut,
    onBoundsChanged,
    bounds,
    ...rectangleOptions
  } = props;
  const callbacks = useRef<Record<string, (e: unknown) => void>>({});
  Object.assign(callbacks.current, {
    onClick,
    onDrag,
    onDragStart,
    onDragEnd,
    onMouseOver,
    onMouseOut,
  });

  const rectangle = useRef(new google.maps.Rectangle()).current;

  const map = useContext(GoogleMapsContext)?.map;

  useMemo(() => {
    rectangle.setOptions(rectangleOptions);
  }, [rectangle, rectangleOptions]);

  useEffect(() => {
    if (!map) {
      if (map === undefined)
        console.error("<Rectangle> has to be inside a Map component.");

      return;
    }

    rectangle.setBounds(bounds);

    rectangle.setMap(map);

    return () => {
      rectangle.setMap(null);
    };
  }, [map, bounds]);

  useEffect(() => {
    if (!rectangle) return;

    const gme = google.maps.event;
    [
      ["click", "onClick"],
      ["drag", "onDrag"],
      ["dragstart", "onDragStart"],
      ["dragend", "onDragEnd"],
      ["mouseover", "onMouseOver"],
      ["mouseout", "onMouseOut"],
    ].forEach(([eventName, eventCallback]) => {
      gme.addListener(rectangle, eventName, (e: google.maps.MapMouseEvent) => {
        const callback = callbacks.current[eventCallback];
        if (callback) callback(e);
      });
    });
    return () => {
      gme.clearInstanceListeners(rectangle);
    };
  }, [rectangle]);

  useEffect(() => {
    const boundsChangeListener = rectangle.addListener("bounds_changed", () => {
      if (onBoundsChanged) {
        const bounds = rectangle.getBounds();
        if (bounds) {
          const newBounds = bounds.toJSON();
          onBoundsChanged(newBounds);
        }
      }
    });

    return () => {
      google.maps.event.removeListener(boundsChangeListener);
    };
  }, [rectangle, onBoundsChanged]);

  return rectangle;
}

export const Rectangle = forwardRef(
  (props: RectangleProps, ref: RectangleRef) => {
    const rectangle = useRectangle(props);

    useImperativeHandle(ref, () => rectangle, []);

    return null;
  }
);
