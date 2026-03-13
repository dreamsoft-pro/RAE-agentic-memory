javascript
// @/lib/utils/copyProperties.js

/**
 * Copies specified properties from a source object to a target object.
 *
 * @param {Object} source - The source object containing the properties to copy.
 * @param {Array<string>} properties - An array of property names to be copied.
 * @param {Object|undefined} [target] - The target object where properties are copied. If not provided, a new empty object is used as default.
 * @returns {Object} The target object with the specified properties copied from the source.
 */
export function copyProperties(source, properties, target) {
    // [BACKEND_ADVICE]
    if (!target) {
        target = {};
    }
    properties.forEach((name) => {
        target[name] = source[name];
    });
    return target;
}

// @/lib/utils/parseFloat.js

/**
 * Parses a string as a floating-point number, replacing commas with dots.
 *
 * @param {string} numberString - The string representation of the number to parse.
 * @returns {number|NaN} The parsed floating point number or NaN if parsing fails.
 */
export function parseFloat(numberString) {
    // [BACKEND_ADVICE]
    if (_.isString(numberString)) {
        numberString = numberString.replace(',', '.');
    }
    return parseFloat(numberString);
}
