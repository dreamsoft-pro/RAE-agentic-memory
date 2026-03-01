import api from "@/lib/api";
import { useEffect } from "react";

interface Factor {
  from: { x: number };
  to: { x: number };
}

interface Props {
  factor: Factor;
  child?: any; // Assuming this is a DOM element or jQuery object, replace with actual type if known
  hProps: string[];
  restore: boolean;
  props2: string[];
  duration: number;
  easing: string;
  mode: "show" | "hide";
  el: any; // Similar to child, assume it's a DOM element or jQuery object
  props: string[];
}

const EffectComponent = (props: Props) => {
  useEffect(() => {
    const animateChildren = async () => {
      if (props.factor.from.x !== props.factor.to.x) {
        const hPropsTransitionStart = await $.effects.setTransition(props.child, props.hProps, props.factor.from.x);
        const hPropsTransitionEnd = await $.effects.setTransition(props.child, props.hProps, props.factor.to.x);

        // Apply transitions and animate
        if (props.child?.css && props.child?.animate) {
          props.child.css(hPropsTransitionStart);
          props.child.animate(
            hPropsTransitionEnd,
            props.duration,
            props.easing,
            async () => {
              if (props.restore) {
                await $.effects.restore(props.child, props.props2);
              }
            }
          );
        }
      }

      // Animate the main element
      const animateMain = async () => {
        props.el.animate(
          { ...props.el.to },
          {
            queue: false,
            duration: props.duration,
            easing: props.easing,
            complete: async function() {
              if (props.el.to.opacity === 0) {
                props.el.css("opacity", props.el.from.opacity);
              }
              if (props.mode === "hide") {
                props.el.hide();
              }
              await $.effects.restore(props.el, props.props);
              if (!props.restore) {
                // Additional logic here
              }
            }.bind(this)
          }
        );
      };

      animateMain().catch(console.error); // Error handling for the main animation
    };

    animateChildren().catch(console.error); // Error handling for children animations

  }, [props.factor, props.child, props.hProps, props.restore, props.props2, props.duration, props.easing, props.mode, props.el, props.props]); // Dependency array ensuring re-render triggers proper effects

  return null; // This component's purpose is side-effect management, no UI to render
};