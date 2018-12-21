function genOption_pie(resource,name){
  window.alert(name)
  console.log(name)
  data = []
  for (prop in resource) {
    data.push({value: resource[prop][1], name: resource[prop][0]})
  }
  var option = {
    tooltip : {
      trigger: 'item',
      formatter: "{a} <br/>{b} : {c}"
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    xAxis: {
      show: false
    },
    yAxis: {
      show: false
    },
    toolbox: {
      feature: {
        saveAsImage: {
          title:'保存'
        }
      }
    },

    series: [{
      name: name,
      type: 'pie',
      radius: '55%',
      data: data
    }]
  }
  return option
}

function genOption_wordCloud(resource){
  data = []
  for (prop in resource) {
    data.push({value: resource[prop][1], name: resource[prop][0]})
  }
  var option = {
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      // maskImage: maskImage,
      left: 'center',
      top: 'center',
      width: '70%',
      height: '80%',
      right: null,
      bottom: null,
      sizeRange: [12, 60],
      rotationRange: [-90, 90],
      rotationStep: 45,
      gridSize: 8,
      drawOutOfBound: false,
      textStyle: {
        normal: {
          fontFamily: 'sans-serif',
          fontWeight: 'bold',
          // Color can be a callback function or a color string
          color: function () {
            // Random color
            return 'rgb(' + [
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160)
            ].join(',') + ')';
          }
        },
        emphasis: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      data: data
    }]
  }
  return option
}

function genOption_funnel(resource){
  data = []
  for (prop in resource) {
    data.push({value: resource[prop][1], name: resource[prop][0]})
  }
  console.log(data)
  var option = {
    tooltip : {
      trigger: 'item',
      formatter: "{a} <br/>{b} : {c}"
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },

    toolbox: {
      feature: {
        saveAsImage: {
          title:'保存'
        }
      }
    },
    calculable: true,
    series: [
      {
        name:'评分',
        type:'funnel',
        left: '20%',
        top: 60,
        //x2: 80,
        bottom: 60,
        width: '70%',
        // height: {totalHeight} - y - y2,
        min: 0,
        max: 100,
        minSize: '30%',
        maxSize: '100%',
        sort: 'descending',
        gap: 2,
        label: {
          normal: {
            show: true,
            position: 'inside'
          },
          emphasis: {
            textStyle: {
              fontSize: 20
            }
          }
        },
        labelLine: {
          normal: {
            length: 10,
            lineStyle: {
              width: 1,
              type: 'solid'
            }
          }
        },
        itemStyle: {
          normal: {
            borderColor: '#fff',
            borderWidth: 1
          }
        },
        data: data
      }]
  }
  return option
}

function genOption_line(resource){
  data = []
  xAxis = resource[0]
  data = resource[1]
  legend = []
  series = []
  for (prop in data) {
    legend.push(prop)
    series.push({
      name: prop,
      type: 'line',
      data: data[prop]
    })
  }
  var option = {
    legend: {
      data: legend
    },
    toolbox: {
      feature: {
        saveAsImage: {
          title:'保存'
        }
      }
    },
    xAxis: {
      data: xAxis
    },
    yAxis: {},
    series: series
  }
  return option
}
