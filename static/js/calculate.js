let findWeights = function(id, weight) {
    arr = [45, 35, 25, 10, 5, 2.5]
    result = []
    i = 0
    if (weight - 45 < 0) {
        return "Your weight is " + (45 - weight) + "lb(s) lighter than the bar"
    }
    if (weight - 45 < 5) {
        //return "Just use the bar. Remainder: " + weight / 2 + " on each side"
        return "Just use the bar. R: " + weight / 2
    }
    else if (weight - 45 == 0) {
        return "Just use the bar"
    }

    weight -= 45

    while (weight !== 0){
        if (i >= arr.length)
            //return "What weights to put on each side of the bar: " + result.join(' ') + " Remainder: " + weight / 2 + " on each side"
            return result.join(' ') + "R: " + weight / 2
        if (weight - arr[i]*2 >= 0){
            weight -= arr[i]*2
            result.push(String(arr[i]))
        }
        else {
            i++
        }
    }
    //return "What weights to put on each side of the bar: " + result.join(' ')
    return result.join(' ')
}

let calculate = function(id, weight) {
    if ($('#result' + id).is(':empty'))
        $('#result' + id).text(findWeights(id, weight))
}

let calculatePercent = function(id, weight, percent){
    pweight = weight * (Number(percent) * 0.01)
    $('#warmupTotal' + id).text("Total: " + pweight)
    $('#warmup' + id).text(findWeights(id, pweight))
}