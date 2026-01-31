import{j as e}from"./jsx-runtime-CDt2p4po.js";import{aT as o,L as r,a8 as b,a9 as S,aU as g}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{R as T}from"./index-GiUgBvb1.js";import{s as i}from"./index.module-B9nxguEg.js";/* empty css               */import"./index-C8NrMXaH.js";const N={title:"React Aria Components/Slider",component:o},l=()=>{const[s,a]=T.useState([30,60]);return e.jsxs("div",{children:[e.jsxs(o,{"data-testid":"slider-example",value:s,onChange:a,style:{position:"relative",display:"flex",flexDirection:"column",alignItems:"center",width:300},children:[e.jsxs("div",{style:{display:"flex",alignSelf:"stretch"},children:[e.jsx(r,{children:"Test"}),e.jsx(b,{style:{flex:"1 0 auto",textAlign:"end"},children:({state:n})=>`${n.getThumbValueLabel(0)} - ${n.getThumbValueLabel(1)}`})]}),e.jsxs(S,{style:{position:"relative",height:30,width:"100%"},children:[e.jsx("div",{style:{position:"absolute",backgroundColor:"gray",height:3,top:13,width:"100%"}}),e.jsx(d,{index:0,children:e.jsx(r,{children:"A"})}),e.jsx(d,{index:1,children:e.jsx(r,{children:"B"})})]})]}),e.jsx("button",{onClick:()=>a([0,100]),children:"reset"})]})},t=s=>e.jsxs(o,{...s,defaultValue:30,className:i.slider,children:[e.jsxs("div",{className:i.label,children:[e.jsx(r,{children:"Test"}),e.jsx(b,{})]}),e.jsx(S,{className:i.track,children:e.jsx(g,{className:i.thumb})})]});t.args={orientation:"horizontal",isDisabled:!1,minValue:0,maxValue:100,step:1};t.argTypes={orientation:{control:{type:"inline-radio",options:["horizontal","vertical"]}}};const d=({index:s,children:a})=>e.jsx(g,{index:s,style:({isDragging:n,isFocusVisible:y})=>({width:20,height:20,borderRadius:"50%",top:"50%",backgroundColor:y?"orange":n?"dimgrey":"gray"}),children:a});l.__docgenInfo={description:"",methods:[],displayName:"SliderExample"};t.__docgenInfo={description:"",methods:[],displayName:"SliderCSS"};var c,u,m;l.parameters={...l.parameters,docs:{...(c=l.parameters)==null?void 0:c.docs,source:{originalSource:`() => {
  const [value, setValue] = React.useState([30, 60]);
  return <div>
      <Slider<number[]> data-testid="slider-example" value={value} onChange={setValue} style={{
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      width: 300
    }}>
        <div style={{
        display: 'flex',
        alignSelf: 'stretch'
      }}>
          <Label>Test</Label>
          <SliderOutput style={{
          flex: '1 0 auto',
          textAlign: 'end'
        }}>
            {({
            state
          }) => \`\${state.getThumbValueLabel(0)} - \${state.getThumbValueLabel(1)}\`}
          </SliderOutput>
        </div>
        <SliderTrack style={{
        position: 'relative',
        height: 30,
        width: '100%'
      }}>
          <div style={{
          position: 'absolute',
          backgroundColor: 'gray',
          height: 3,
          top: 13,
          width: '100%'
        }} />
          <CustomThumb index={0}>
            <Label>A</Label>
          </CustomThumb>
          <CustomThumb index={1}>
            <Label>B</Label>
          </CustomThumb>
        </SliderTrack>
      </Slider>
      <button onClick={() => setValue([0, 100])}>reset</button>
    </div>;
}`,...(m=(u=l.parameters)==null?void 0:u.docs)==null?void 0:m.source}}};var p,h,x;t.parameters={...t.parameters,docs:{...(p=t.parameters)==null?void 0:p.docs,source:{originalSource:`props => <Slider {...props} defaultValue={30} className={styles.slider}>
    <div className={styles.label}>
      <Label>Test</Label>
      <SliderOutput />
    </div>
    <SliderTrack className={styles.track}>
      <SliderThumb className={styles.thumb} />
    </SliderTrack>
  </Slider>`,...(x=(h=t.parameters)==null?void 0:h.docs)==null?void 0:x.source}}};const w=["SliderExample","SliderCSS"];export{t as SliderCSS,l as SliderExample,w as __namedExportsOrder,N as default};
