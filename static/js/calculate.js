let findWeights = function(id, weight) {
    arr = [45, 35, 25, 10, 5, 2.5]
    result = []
    i = 0

    weight -= 45

    if (weight <= 0) {
        return 0
    }

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
    return result.join('<br>')
}

let calWeights = function(id, weight) {
    if (($('#weightsLeft' + id).is(':empty') || $('#weightsRight' + id).is(':empty'))) {
        weights = findWeights(id, weight)
        $('#weightsLeft' + id).html(weights)
        $('#weightsRight' + id).html(weights)
    }
}

let calPercent = function(id, weight, percent){
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
