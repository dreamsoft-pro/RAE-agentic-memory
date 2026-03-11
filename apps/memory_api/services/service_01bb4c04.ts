import api from '@/lib/api';

interface EffectArgs {
  mode?: string;
  queue?: boolean | string;
  effect: string;
  duration?: number | Function;
  complete?: (this: HTMLElement) => void;
}

class EffectsManager {

  private static _normalizeArguments(...args: any[]): EffectArgs {
    let options: EffectArgs = {};
    
    if (typeof args[0] === "string" && !EffectsManager._isStandardEffect(args[0])) return true;
    if ($.isFunction(args[0])) return true;
    if (typeof args[0] === 'object' && !args[0].effect) return true;

    options.effect = args.shift();
    
    const lastArg = args.pop();

    // Remaining arguments are speed, callback and/or extra settings
    options.duration = args.length ? typeof args[args.length - 1] === "function" ? args.pop() : args[args.length - 1] : undefined;
    options.complete = $.isFunction(lastArg) ? lastArg : undefined;

    return options as EffectArgs;
  }

  private static _isStandardEffect(effect: string): boolean {
    // Assuming this checks if an effect is a standard one
    return false; // Placeholder implementation
  }

  public async applyEffect(element: HTMLElement, ...args: any[]): Promise<void> {
    const argsObject = EffectsManager._normalizeArguments(...args);
    
    const mode = argsObject.mode;
    const queue = argsObject.queue;
    const effectMethod = $.effects.effect[argsObject.effect];
    
    if ($.fx.off || !effectMethod) {
      if (mode) {
        return element[mode](argsObject.duration, argsObject.complete);
      } else {
        element.addEventListener('transitionend', () => {
          if (argsObject.complete) {
            argsObject.complete.call(element);
          }
        });
      }
    }

    // Apply custom effect logic here
  }

}

// Usage example:
const effectsManager = new EffectsManager();
document.getElementById("myElement").addEventListener('click', async () => {
  await effectsManager.applyEffect(document.getElementById("anotherElement"), 'fadeToggle');
});