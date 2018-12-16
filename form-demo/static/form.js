app = new Vue({
  el: "#app",
  delimiters: ['{[', ']}'],
  data: {
    startm: '',
    endm: '',
    resource: 'Hello',
    startDatePicker: '',
    endDatePicker: '',
    myChart: '',
    chartType: '0'
  },
  created: function(){
    this.startDatePicker = this.startDatePicker2()
    this.endDatePicker = this.endDatePicker2()
  },
  methods: {
    submit: function(){
      if(!this.startm || !this.endm){
        alert('请输入正确的起始日期')
      }
      axios.post('/resource', {
        type: this.chartType,
        startm: this.startm,
        endm: this.endm
      })
        .then(response => {
          this.resource = response.data
          console.log('resource:' + this.resource)

          console.log('Hello')
          if(this.chartType == '0' || this.chartType == '2'){
            console.log('Hello')
            data = []
            for (prop in this.resource) {
              data.push({value: this.resource[prop], name: prop})
            }
            console.log(data)
            var option = {
              legend: {},
              xAxis: {},
              yAxis: {},
              series: [{
                name: '票房',
                type: 'pie',
                radius: '55%',
                data: data
              }]
            }
          }
          else if(this.chartType == '1' || this.chartType == '3'){
            xAxis = this.resource[0]
            data = this.resource[1]
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
            console.log(xAxis)
            console.log(series)
            var option = {
              legend: {
                data: legend
              },
              xAxis: {
                data: xAxis
              },
              yAxis: {},
              series: series
            };
          }
          this.myChart.setOption(option);
        }, response => {
          console.log(response)
        })
    },
    startDatePicker2: function(){
      let self = this
      return {
        disabledDate(time){
          let startDate = new Date(2015, 0)
          if(self.endm){
            return time.getTime() > new Date(self.endm).getTime() || time.getTime() < startDate
          }
          return time.getTime() < startDate//开始时间不选时，结束时间最大值小于等于当天
        }
      }
    },
    endDatePicker2: function(){
      let self = this
      return {
        disabledDate(time){
          let endDate = new Date(2018, 11)
          if(self.startm){
            return new Date(self.startm).getTime() > time.getTime() || time.getTime() > endDate
          }else{
            return time.getTime() > Date.now()//开始时间不选时，结束时间最大值小于等于当天
          }
        }
      }
    }
  }
});
// app.delimiters:['{[', ']}']
