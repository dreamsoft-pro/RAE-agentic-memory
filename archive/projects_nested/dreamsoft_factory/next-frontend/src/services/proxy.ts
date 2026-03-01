import { NextRequest, NextResponse } from "next/server";

/**
 * Modernized Proxy Middleware for Next.js 14+
 * Built by the Council of Elders (Claude 4.5 + GPT-4o)
 */

const URL_MAP: Record<string, string> = {
    "/35/images/favicon.ico": "/favicon.ico",
    "/templates/default/1/footer.html": "/views/footer.html",
    "/templates/default/2/content.html": "/src/index/templates/content.html",
    "/templates/default/3/header.html": "/views/header.html",
    "/templates/default/4/slider.html": "/views/slider.html",
    "/templates/default/5/footer-news.html": "/views/footer-news.html",
    "/templates/default/6/footer-links.html": "/views/footer-links.html",
    "/templates/default/8/cart.html": "/src/cart/templates/cart.html",
    "/templates/default/9/main.html": "/views/main.html",
    "/templates/default/10/login.html": "/src/index/templates/login.html",
    "/templates/default/11/register.html": "/src/index/templates/register.html",
    "/templates/default/12/password-remind.html": "/src/index/templates/password-remind.html",
    "/templates/default/13/news.html": "/src/index/templates/news.html",
    "/templates/default/14/contact.html": "/src/index/templates/contact.html",
    "/templates/default/22/client-zone.html": "/src/client-zone/templates/client-zone.html",
    "/templates/default/24/client-zone-orders.html": "/src/client-zone/templates/client-zone-orders.html",
    "/templates/default/27/client-zone-reclamations.html": "/src/client-zone/templates/client-zone-reclamations.html",
    "/templates/default/28/category.html": "/src/category/templates/category.html",
    "/templates/default/29/group.html": "/src/category/templates/group.html",
    "/templates/default/30/calc.html": "/src/category/templates/calc.html",
    "/templates/default/31/address-modal.html": "/src/category/templates/modalboxes/address-modal.html",
    "/templates/default/33/cart-verify.html": "/src/cart/templates/cart-verify.html",
    "/templates/default/34/upload-files.html": "/src/cart/templates/modalboxes/upload-files.html",
    "/templates/default/35/confirm-modal.html": "/views/modalboxes/confirm.html",
    "/templates/default/37/logout-in-progress.html": "/src/index/templates/logout-in-progress.html",
    "/templates/default/62/client-zone-data.html": "/src/client-zone/templates/client-zone-data.html",
    "/templates/default/63/client-zone-change-pass.html": "/src/client-zone/templates/client-zone-change-pass.html",
    "/templates/default/64/client-zone-invoice-data.html": "/src/client-zone/templates/client-zone-invoice-data.html",
    "/templates/default/65/edit-delivery-address.html": "/src/client-zone/templates/modalboxes/edit-delivery-address.html",
    "/templates/default/66/client-zone-delivery-data.html": "/src/client-zone/templates/client-zone-delivery-data.html",
    "/templates/default/67/show-delivery-modal.html": "/src/cart/templates/modalboxes/show-delivery.html",
    "/templates/default/68/order-address-list.html": "/src/client-zone/templates/modalboxes/order-addresses-list.html",
    "/templates/default/72/payment-modal.html": "/src/client-zone/templates/modalboxes/payment.html",
    "/templates/default/73/printoffer-modal.html": "/src/category/templates/modalboxes/printoffer.html"
};

export async function middleware(request: NextRequest) {
    const { pathname } = request.nextUrl;
    
    if (URL_MAP[pathname]) {
        const url = request.nextUrl.clone();
        url.pathname = URL_MAP[pathname];
        return NextResponse.rewrite(url);
    }

    return NextResponse.next();
}

export const config = {
    matcher: ["/templates/:path*", "/35/images/:path*"],
};
