app = new Vue({
  el: "#app",
  delimiters: ['{[', ']}'],
  data: {
    startm: '',
    endm: '',
    resource: 'Hello',
    startDatePicker: '',
    endDatePicker: '',
    mychart: ''
  },
  created: function(){
    this.startDatePicker = this.startDatePicker2()
    this.endDatePicker = this.endDatePicker2()
  },
  methods: {
    submit: function(){
      axios.post('/resource', {
        startm: this.startm,
        endm: this.endm
      })
        .then(response => {
          this.resource = response.data
          console.log('resource:' + this.resource)

          data = []
          for (prop in this.resource) {
            data.push({value: this.resource[prop], name: prop})
          }
          console.log(data)
          var option = {
            series: [{
              name: '票房',
              type: 'pie',
              radius: '55%',
              data: data
            }]
          }
          this.myChart.setOption(option);
          //this.$set('resource', response.data)
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
