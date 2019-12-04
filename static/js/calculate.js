let findWeights = function(id, weight) {
    arr = [45, 35, 25, 10, 5, 2.5]
    result = []
    i = 0
    if (weight < 45) {
        return "Your weight is " + (45 - weight) + "lb(s) lighter than the bar"
    }
    if (weight < 50) {
        //return "Just use the bar. Remainder: " + weight / 2 + " on each side"
        return "Just use the bar. R: " + Number((weight / 2).toFixed(1))
    }
    else if (weight == 45) {
        return "Just use the bar"
    }

    weight -= 45

    while (weight !== 0) {
        if (i >= arr.length)
            return result.join('<br>') + "<br>R: " + Number((weight / 2).toFixed(1))

        if (weight - arr[i]*2 >= 0) {
            weight -= arr[i]*2
            result.push(String(arr[i]))
        }
        else {
            i++
        }
    }
    //return "What weights to put on each side of the bar: " + result.join(' ')
    return result.join('<br>')
}

let calculate = function(id, weight) {
    if (weight > 2000) {
        alert("There's no way your lifting that much weight!")
        return
    }

    if ($('#resultLeft' + id).is(':empty') || $('#resultRight' + id).is(':empty')) {
        weights = findWeights(id, weight)
        $('#resultLeft' + id).html(weights)
        $('#resultRight' + id).html(weights)
    }
}

let calculatePercent = function(id, weight, percent){
    if (percent === '') {
        alert('Please input percent')
        return
    }
    if (percent.search(/\D|(^0+$)/) != -1) {
        alert('Percent must be a positive integer')
        return
    }

    percent = Number(percent)

    if (percent >= 100) {
        alert('Percent must be less than 100')
        return
    }

    warmpWeight = Number((weight * (percent * 0.01)).toFixed(2))
    $('#warmupTotal' + id).text("Total: " + warmpWeight)

    weights = findWeights(id, warmpWeight)
    $('#warmupLeft' + id).html(weights)
    $('#warmupRight' + id).html(weights)
}
