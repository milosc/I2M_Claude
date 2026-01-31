import{j as p}from"./jsx-runtime-CDt2p4po.js";import{C as m}from"./ColorSwatch-C5hr6lpG.js";/* empty css               */import"./index-GiUgBvb1.js";const S={title:"React Aria Components/ColorSwatch",component:m},e=r=>p.jsx(m,{...r,style:({color:t})=>({width:32,height:32,borderRadius:4,boxShadow:"inset 0 0 0 1px rgba(0, 0, 0, 0.1)",background:`
        linear-gradient(${t}, ${t}),
        repeating-conic-gradient(#CCC 0% 25%, white 0% 50%) 50% / 16px 16px`})}),o={render:r=>p.jsx(e,{...r}),args:{color:"rgb(255, 0, 0)"},argTypes:{color:{control:"color"}}};e.__docgenInfo={description:"",methods:[],displayName:"ColorSwatchExampleRender",props:{className:{required:!1,tsType:{name:"union",raw:"string | ((values: T & {defaultClassName: string | undefined}) => string)",elements:[{name:"string"},{name:"unknown"}]},description:"The CSS [className](https://developer.mozilla.org/en-US/docs/Web/API/Element/className) for the element. A function may be provided to compute the class based on component state."},style:{required:!1,tsType:{name:"union",raw:"CSSProperties | ((values: T & {defaultStyle: CSSProperties}) => CSSProperties | undefined)",elements:[{name:"CSSProperties"},{name:"unknown"}]},description:"The inline [style](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style) for the element. A function may be provided to compute the style based on component state."},slot:{required:!1,tsType:{name:"union",raw:"string | null",elements:[{name:"string"},{name:"null"}]},description:"A slot name for the component. Slots allow the component to receive props from a parent component.\nAn explicit `null` value indicates that the local props completely override all props received from a parent."}},composes:["AriaColorSwatchProps","GlobalDOMAttributes"]};var n,a,s;e.parameters={...e.parameters,docs:{...(n=e.parameters)==null?void 0:n.docs,source:{originalSource:`(args: ColorSwatchProps): JSX.Element => <ColorSwatch {...args} style={({
  color
}) => ({
  width: 32,
  height: 32,
  borderRadius: 4,
  boxShadow: 'inset 0 0 0 1px rgba(0, 0, 0, 0.1)',
  background: \`
        linear-gradient(\${color}, \${color}),
        repeating-conic-gradient(#CCC 0% 25%, white 0% 50%) 50% / 16px 16px\`
})} />`,...(s=(a=e.parameters)==null?void 0:a.docs)==null?void 0:s.source}}};var l,i,c;o.parameters={...o.parameters,docs:{...(l=o.parameters)==null?void 0:l.docs,source:{originalSource:`{
  render: args => <ColorSwatchExampleRender {...args} />,
  args: {
    color: 'rgb(255, 0, 0)'
  },
  argTypes: {
    color: {
      control: 'color'
    }
  }
}`,...(c=(i=o.parameters)==null?void 0:i.docs)==null?void 0:c.source}}};const C=["ColorSwatchExampleRender","ColorSwatchExample"];export{o as ColorSwatchExample,e as ColorSwatchExampleRender,C as __namedExportsOrder,S as default};
