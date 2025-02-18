<template>
    <div class="image-map-container">
        <img src='@/assets/body.jpg' usemap="#image-map" @load="onImageLoad" class="custom-image-size"/>
       {{buwei}}
        <div
            v-if="hoverArea"
            class="overlay"
            :style="overlayStyle"
        ></div>

        <map name="image-map">
            <!-- Example for one area, add mouseenter and mouseleave -->
    <area target="" alt="头" title="头"  coords="156,14,164,22,166,31,171,44,164,57,161,62,156,65,151,69,141,65,132,62,129,56,127,47,125,39,126,28,129,19,138,12,148,9" shape="poly"  @mouseenter="onMouseEnter($event, '头部')" @mouseleave="onMouseLeave" @click="areaclick('头部')">
    <area target="" alt="左脚" title="左脚"  coords="104,423,114,422,120,422,125,423,126,431,125,440,120,447,113,458,101,459,90,456,90,445,100,435" shape="poly" @mouseenter="onMouseEnter($event, '左脚')" @mouseleave="onMouseLeave" @click="areaclick('左脚')" >
    <area target="" alt="右脚" title="右脚"  coords="171,422,177,422,185,423,193,422,197,428,199,437,206,445,208,455,199,460,189,460,181,452,178,444,172,435" shape="poly" @mouseenter="onMouseEnter($event, '右脚')" @mouseleave="onMouseLeave" @click="areaclick('右脚')">
    <area target="" alt="喉咙" title="喉咙"  coords="130,68,137,68,147,70,154,68,163,66,163,72,164,76,165,84,148,85,132,86,131,77" shape="poly" @mouseenter="onMouseEnter($event, '颈部')" @mouseleave="onMouseLeave" @click="areaclick('喉咙')">
    <area target="" alt="胸部" title="胸部"  coords="116,90,113,105,110,121,109,136,110,154,125,150,137,149,150,151,164,150,174,151,183,156,188,145,188,123,185,106,177,89" shape="poly" @mouseenter="onMouseEnter($event, '胸部')" @mouseleave="onMouseLeave" @click="areaclick('胸部')">
    <area target="" alt="腹部" title="腹部"  coords="112,156,110,174,110,186,123,189,147,189,174,191,188,188,186,159,147,153" shape="poly" @mouseenter="onMouseEnter($event, '腹部')" @mouseleave="onMouseLeave" @click="areaclick('腹部')">
    <area target="" alt="生殖" title="生殖"  coords="110,189,121,192,139,193,155,193,172,194,184,194,190,193,190,200,192,214,195,230,198,241,162,244,143,245,109,242,98,238,102,212" shape="poly" @mouseenter="onMouseEnter($event, '生殖区')" @mouseleave="onMouseLeave" @click="areaclick('生殖区')">
    <area target="" alt="左腿" title="左腿"  coords="97,240,120,248,147,247,133,337,138,358,127,396,125,419,107,419,103,392,98,355,105,315,96,281" shape="poly" @mouseenter="onMouseEnter($event, '左下肢')" @mouseleave="onMouseLeave" @click="areaclick('左下肢')">
    <area target="" alt="右腿" title="右腿"  coords="151,246,176,245,198,244,200,272,193,302,198,348,196,364,192,420,172,419,173,403,160,356,163,336,157,312" shape="poly" @mouseenter="onMouseEnter($event, '右下肢')" @mouseleave="onMouseLeave" @click="areaclick('右下肢')">
    <area target="" alt="右臂" title="右臂"  coords="180,90,188,108,192,144,210,184,229,204,234,214,244,243,256,250,268,249,280,241,274,227,278,214,249,203,239,170,226,147,215,125,212,101,198,90" shape="poly" @mouseenter="onMouseEnter($event, '右上肢')" @mouseleave="onMouseLeave" @click="areaclick('右上肢')">
    <area target="" alt="左臂" title="左臂"  coords="113,88,97,91,88,102,84,113,84,120,76,139,62,163,49,202,24,212,17,217,26,222,22,241,31,250,49,249,68,205,90,179,95,161,105,147" shape="poly" @mouseenter="onMouseEnter($event, '左上肢')" @mouseleave="onMouseLeave" @click="areaclick('左上肢')">
            <!-- Repeat for other areas, ensure to add mouse event handlers -->
        </map>
    </div>
</template>
<script>
export default {
    data() {
        return {
            hoverArea: null, // 当前悬停的区域
            buwei:''
        };
    },
    methods: {
        areaclick(area) {
            // console.log(area);
            this.buwei=area
           
        },
        onImageLoad(event) {
            // 图片加载后的逻辑
        },
        onMouseEnter(event, area) {
            // this.buwei=area
            this.hoverArea = {
                coords: event.target.coords
            };
        },
        onMouseLeave() {
            this.hoverArea = null;
        }
    },
    computed: {
        overlayStyle() {
            if (!this.hoverArea) return {};
            const coords = this.hoverArea.coords.split(',').map(Number);
            const minX = Math.min(...coords.filter((_, i) => i % 2 === 0));
            const minY = Math.min(...coords.filter((_, i) => i % 2 === 1));
            const maxX = Math.max(...coords.filter((_, i) => i % 2 === 0));
            const maxY = Math.max(...coords.filter((_, i) => i % 2 === 1));
            return {
                left: `${minX}px`,
                top: `${minY}px`,
                width: `${maxX - minX}px`,
                height: `${maxY - minY}px`,
                display: 'block',
                position: 'absolute',
                backgroundColor: 'rgba(0, 0, 255, 0.5)', // 半透明蓝色
                border: '1px solid blue'
            };
        }
    }
};


</script>
<style>

.image-map-container {
    position: relative;
}
.overlay {
    position: absolute;
    pointer-events: none; /* Ensure overlay does not interfere with image map interaction */
}

</style>
