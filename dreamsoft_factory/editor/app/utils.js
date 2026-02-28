export function safeImage() {
    const img = new Image();
    img.crossOrigin = 'Anonymous';
    return img;
}
/**
 *
 * @param source Object
 * @param properties Array
 * @param target Object|undefined
 */
_.copyProperties=function(source,properties,target){
    if(!target){
        target={}
    }
    properties.forEach(function(name){
        target[name]=source[name]
    });
    return target
}
