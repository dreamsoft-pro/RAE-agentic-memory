javascript
// [BACKEND_ADVICE] This logic should be reviewed for backend integration.
export const priceFilter = (value) => {
  if (value === parseInt(value, 10)) {
    return `${value},00`;
  }
  return value;
};

// @/lib/api/price-filter.js
import { priceFilter } from './helpers';

const applyPriceFilter = (value) => {
  return '@/lib/api'.apply(priceFilter, [value]);
};

export default applyPriceFilter;
