javascript
import { apiRequest } from '@/lib/api';

const CouponService = {};

function getResource() {
    return ['dp_coupons'];
}

CouponService.check = function (coupon, orderID) {
    const resource = getResource();
    resource.push('check');

    // [BACKEND_ADVICE] Heavy logic here
    return apiRequest({
        method: 'POST',
        url: `${import.meta.env.VITE_API_URL}/${resource.join('/')}`,
        data: {
            coupon,
            orderID
        }
    });
};

export default CouponService;
