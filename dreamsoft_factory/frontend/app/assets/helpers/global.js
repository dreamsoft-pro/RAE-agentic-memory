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

_.parseFloat=function(numberString){
    if(_.isString(numberString)){
        numberString=numberString.replace(',','.')
    }
    return parseFloat(numberString)
}
