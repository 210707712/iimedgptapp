<template>
  <div style="margin: 2%;">
    <button @click="filterAllZero">非可能疾病</button>
    <button @click="filterNotAllZero">可能疾病</button>
    <button @click="clearFilter">清除筛选</button>
    <table>
      <thead>
        <tr>
          <th>疾病名称</th>
          <th colspan="7">症状</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in filteredData" :key="item.name">
          <td style="background-color:burlywood">{{ item.name }}</td>
          <td v-for="symptom in item.symptoms" :key="symptom.name" :style="{ backgroundColor: symptom.flag == 0 ? 'green' : 'red' }">
            {{ symptom.symptom }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import tableData from '@/assets/flag_data.json'; // Adjust the path as necessary

export default {
  data() {
    return {
      tableData,
      filterType: null // 'allZero', 'notAllZero', or null
    };
  },
  computed: {
    filteredData() {
      if (this.filterType === 'allZero') {
        return this.tableData.filter(item =>
          item.symptoms.every(symptom => symptom.flag === '0')
        );
      } else if (this.filterType === 'notAllZero') {
        return this.tableData.filter(item =>
          item.symptoms.some(symptom => symptom.flag !== '0')
        );
      }
      return this.tableData;
    }
  },
  methods: {
    filterAllZero() {
      this.filterType = 'allZero';
    },
    filterNotAllZero() {
      this.filterType = 'notAllZero';
    },
    clearFilter() {
      this.filterType = null;
    }
  }

}

</script>
<style>
table {
  width: 100%;
  border-collapse: collapse;
  background: linear-gradient(to right, #f9f9f9, #eef1f5);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  text-align: left;
}

th {
  background-color: #607d8b;
  color: white;
  font-weight: bold;
}

tbody tr:nth-child(odd) {
  background-color: #f4f4f4;
}

tbody tr:hover {
  background-color: #ddd;
}

ul {
  padding: 0;
  list-style: none;
}

li {
  padding: 2px 0;
}
</style>
