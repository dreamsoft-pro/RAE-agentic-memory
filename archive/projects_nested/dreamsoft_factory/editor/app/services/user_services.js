function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

const services = function (editor) {

    const Editor = editor;

    const calculatePrice = () => {
        const obj = Editor.userProject.getObj();
        if (!obj) return null;

        const isComplex = Editor.userProject.isComplex();
        const attributes = [];

        if (isComplex) {
            const products = obj.projects.map((project, index) => {
                const selectedAttributes = Editor.selectedProductAttributes[index];

                const options = Object.keys(selectedAttributes)
                    .filter(key => key !== 'typeID')
                    .map(key => ({attrID: key, optID: selectedAttributes[key]}));

                return {
                    typeID: project.typeID,
                    formatID: project.Format.formatID,
                    width: project.Format.width,
                    height: project.Format.height,
                    pages: Editor.userProject.getPagesCountForProduct(index),
                    options
                };
            });

            calculatePriceRequest(products, Editor.getProductId());
        } else {
            const options = Object.keys(obj.selectedAttributes)
                .filter(key => key !== 'typeID')
                .map(key => ({attrID: key, optID: obj.selectedAttributes[key]}));

            const singleProduct = [{
                typeID: obj.typeID,
                formatID: obj.Format.formatID,
                width: obj.Format.width,
                height: obj.Format.height,
                options,
                pages: Editor.userProject.getAllPagesCount()
            }];

            calculatePriceRequest(singleProduct, obj.typeID);
        }
    };

    const calculatePriceRequest = (products, typeID) => {
        $.ajax({
            url: `${EDITOR_ENV.frameworkUrl}/ps_groups/${Editor.productData[0].products[0].groupID}/ps_types/${Editor.productData[0].products[0].baseID}/ps_calculate/calculatePublic`,
            type: "POST",
            headers: {
                "access-token": getCookie('access-token')
            },
            data: {
                amount: 1,
                typeID,
                products,
                volume: 1,
                currency: "PLN"
            },
            success: (resp) => {
                Editor.lastCalculation = resp;
                const thickness = resp.products.reduce((total, elem) => total + elem.thickness, 0);
                Editor.userProject.updateCoverHeight(thickness);

                const prevText = $('#orderPrice').text();
                const prevPrice = prevText.indexOf(" ") !== -1 ? prevText.substring(prevText.indexOf(' ') + 1, prevText.lastIndexOf(' ')) : 0;

                if (prevPrice !== resp.calculation.price && ['advancedUser', 'advancedAdmin'].some(c => c === editor.userType)) {
                    $("#orderPrice")
                        .html(`${resp.calculation.price}zł`)
                        .show()
                        .animate({
                            opacity: 1,
                            width: "100%"
                        }, 300, () => {
                            setTimeout(() => {
                                $("#orderPrice")
                                    .animate({
                                        width: 0,
                                        opacity: 0
                                    }, 300, () => {
                                        $("#orderPrice").hide()
                                        $('#orderPrice')[0].innerHTML = `Zamów ${resp.calculation.price} zł`;
                                    })
                            }, 300)
                        })
                } else {
                    $('#orderPrice')[0].innerHTML = `Zamów ${resp.calculation.price} zł`;
                }
            }
        });
    };

    const addToCart = () => {
        const obj = Editor.userProject.getObj();

        if (!obj) return null;

        const products = obj.projects.map((project, index) => {
            const attributes = Object.keys(Editor.selectedProductAttributes[index])
                .filter(key => key !== 'typeID')
                .map(key => ({
                    attrID: key,
                    optID: Editor.selectedProductAttributes[index][key]
                }));

            return {
                typeID: project.typeID,
                formatID: project.Format.formatID,
                width: project.Format.width,
                height: project.Format.height,
                pages: Editor.userProject.getPagesCountForProduct(index),
                options: attributes
            };
        });

        const requestData = {
            amount: 1,
            volume: 1,
            typeID: Editor.getProductId(),
            products,
            currency: "PLN",
            projectID: Editor.userProject.getID(),
            orderID: Editor.getURLParameters()['orderID'],
            productID: Editor.getURLParameters()['productID'],
            inEditor: 2
        };

        addToCartRequest(
            `${EDITOR_ENV.frameworkUrl}/ps_groups/${Editor.productData[0].products[0].groupID}/ps_types/${Editor.productData[0].products[0].baseID}/ps_calculate/saveCalculationPublic`,
            requestData
        );
    }

    const addToCartRequest = (url, data) => {
        $.ajax({
            url,
            type: "POST",
            headers: {
                "access-token": getCookie('access-token'),
                "domain-name": EDITOR_ENV.domain.substring(EDITOR_ENV.domain.indexOf('//') + 2),
            },
            data,
            success: function (resp) {
                if (resp.response) {
                    addToCartPost(resp);
                } else {
                    alert('Nie udało się dodać do koszyka, skontaktuj się z administratorem.');
                }
            }
        });
    }

    function addToCartPost(resp) {
        $.ajax({
            type: 'POST',
            url: `${EDITOR_ENV.authUrl}/cart/add?domainName=${EDITOR_ENV.domain.replace(/http(s)?:\/\//, '')}`,
            data: {
                calcID: resp.calcID,
                orderID: resp.orderID,
                productID: resp.productID
            },
            headers: {
                "access-token": getCookie('access-token'),
            },
            success: function () {
                window.location = `${EDITOR_ENV.frontendUrl}${resp.cartUrl}`;
            },
        });
    }


    return {
        calculatePrice: calculatePrice,
        addToCart: addToCart,
    };
}

export {services};
