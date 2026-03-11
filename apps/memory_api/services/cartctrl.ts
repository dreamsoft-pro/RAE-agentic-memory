javascript
import '@/lib/api';

let isCollapsed = false;
let cart = {};
let deliveries = [];
let addresses = [];
let blockCart = false;
let payments = [];
let preventPayment = false;
let paymentsOffset = 0;
let countries = [];
let coupons = [];
let onlyForCompanies = false;
let confirmButtonInCart = false;
let userCanRecalculateCart = false;
let reCountProductExist = false;
let confirmTextInCart = {};
let senders = [];
let confirmButton = false;
let showSeparateConfirmButton = false;

let form = {};
let noRegisterForm = {};

let canJoinAddresses = false;
let addressToJoin = {};

let connectedIndexes = {};
let connectDeliveryPrices = {};

let joinedDelivery = {};

// [BACKEND_ADVICE] Consider moving timeout logic to backend for better management
let _timeout;
let _overallTimeout;

export default {
    isCollapsed,
    cart,
    deliveries,
    addresses,
    blockCart,
    payments,
    preventPayment,
    paymentsOffset,
    countries,
    coupons,
    onlyForCompanies,
    confirmButtonInCart,
    userCanRecalculateCart,
    reCountProductExist,
    confirmTextInCart,
    senders,
    confirmButton,
    showSeparateConfirmButton,
    form,
    noRegisterForm,
    canJoinAddresses,
    addressToJoin,
    connectedIndexes,
    connectDeliveryPrices,
    joinedDelivery
};
