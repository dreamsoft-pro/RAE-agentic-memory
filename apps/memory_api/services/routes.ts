/**
 * Modernized Routes Configuration for Next.js 14+
 * Built by the Council of Elders (Claude 4.5 + GPT-4o)
 */

export const ROUTES = {
    HOME: "/",
    LOGIN: "/login",
    REGISTER: "/register",
    PASSWORD_REMIND: "/password-remind",
    CONTACT: "/contact",
    NEWS: "/news",
    CATEGORY: (id: string) => `/category/${id}`,
    PRODUCT: (categoryId: string, productId: string) => `/category/${categoryId}/product/${productId}`,
    CLIENT_ZONE: {
        ROOT: "/client-zone",
        ORDERS: "/client-zone/orders",
        DATA: "/client-zone/data",
        RECLAMATIONS: "/client-zone/reclamations",
        PHOTOS: "/client-zone/my-photos",
        PROJECTS: "/client-zone/my-projects",
    },
    CART: {
        ROOT: "/cart",
        VERIFY: "/cart/verify",
    }
};

export type AppRoute = typeof ROUTES;
