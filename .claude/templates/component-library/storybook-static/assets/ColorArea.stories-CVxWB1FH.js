import{j as t}from"./jsx-runtime-CDt2p4po.js";import{a5 as E,a6 as v}from"./Virtualizer-43kePMo2.js";import{b as w}from"./ColorSwatch-C5hr6lpG.js";import{r as N}from"./index-GiUgBvb1.js";import{ColorSliderExampleRender as _}from"./ColorSlider.stories-DfIqYbEK.js";/* empty css               */import"./index-C8NrMXaH.js";const q={title:"React Aria Components/ColorArea",decorators:[(a,e)=>{var d;let n=e.args,[r,i]=N.useState(w(((d=n.defaultValue)==null?void 0:d.toString())??"")),R=r.getColorChannels().find(p=>p!==n.xChannel&&p!==n.yChannel);return t.jsxs("div",{style:{display:"flex",flexDirection:"column",gap:8},children:[a({...e,args:{...e.args,value:r,onChange:i}}),t.jsx(_,{channel:R,value:r,onChange:i})]})}],component:E,excludeStories:["ColorAreaExampleRender"]},c=192,u=28,h=20,j=4,T=a=>t.jsx(E,{...a,style:({isDisabled:e})=>({width:c,height:c,borderRadius:j,opacity:e?.3:void 0}),children:t.jsx(v,{style:({color:e,isDisabled:n,isFocusVisible:r})=>({background:n?"rgb(142, 142, 142)":e.toString(),border:`2px solid ${n?"rgb(142, 142, 142)":"white"}`,borderRadius:"50%",boxShadow:"0 0 0 1px black, inset 0 0 0 1px black",boxSizing:"border-box",height:r?u+4:h,transform:"translate(-50%, -50%)",width:r?u+4:h})})}),o={render:a=>t.jsx(T,{...a}),args:{defaultValue:"rgb(100, 149, 237)",xChannel:"red",yChannel:"green"},argTypes:{xChannel:{control:"select",options:["red","green","blue"]},yChannel:{control:"select",options:["red","green","blue"]}}},s={render:o.render,args:{defaultValue:"hsl(219, 79%, 66%)",xChannel:"hue",yChannel:"saturation"},argTypes:{xChannel:{control:"select",options:["hue","saturation","lightness"]},yChannel:{control:"select",options:["hue","saturation","lightness"]}}},l={render:o.render,args:{defaultValue:"hsb(219, 79%, 66%)",xChannel:"hue",yChannel:"saturation"},argTypes:{xChannel:{control:"select",options:["hue","saturation","brightness"]},yChannel:{control:"select",options:["hue","saturation","brightness"]}}};T.__docgenInfo={description:"",methods:[],displayName:"ColorAreaExampleRender",props:{className:{required:!1,tsType:{name:"union",raw:"string | ((values: T & {defaultClassName: string | undefined}) => string)",elements:[{name:"string"},{name:"unknown"}]},description:"The CSS [className](https://developer.mozilla.org/en-US/docs/Web/API/Element/className) for the element. A function may be provided to compute the class based on component state."},style:{required:!1,tsType:{name:"union",raw:"CSSProperties | ((values: T & {defaultStyle: CSSProperties}) => CSSProperties | undefined)",elements:[{name:"CSSProperties"},{name:"unknown"}]},description:"The inline [style](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style) for the element. A function may be provided to compute the style based on component state."},children:{required:!1,tsType:{name:"union",raw:"ReactNode | ((values: T & {defaultChildren: ReactNode | undefined}) => ReactNode)",elements:[{name:"ReactNode"},{name:"unknown"}]},description:"The children of the component. A function may be provided to alter the children based on component state."},slot:{required:!1,tsType:{name:"union",raw:"string | null",elements:[{name:"string"},{name:"null"}]},description:"A slot name for the component. Slots allow the component to receive props from a parent component.\nAn explicit `null` value indicates that the local props completely override all props received from a parent."}},composes:["AriaColorAreaProps","GlobalDOMAttributes"]};var m,C,g;o.parameters={...o.parameters,docs:{...(m=o.parameters)==null?void 0:m.docs,source:{originalSource:`{
  render: args => <ColorAreaExampleRender {...args} />,
  args: {
    defaultValue: 'rgb(100, 149, 237)',
    xChannel: 'red',
    yChannel: 'green'
  },
  argTypes: {
    xChannel: {
      control: 'select',
      options: ['red', 'green', 'blue']
    },
    yChannel: {
      control: 'select',
      options: ['red', 'green', 'blue']
    }
  }
}`,...(g=(C=o.parameters)==null?void 0:C.docs)==null?void 0:g.source}}};var x,f,y;s.parameters={...s.parameters,docs:{...(x=s.parameters)==null?void 0:x.docs,source:{originalSource:`{
  render: ColorAreaExample.render,
  args: {
    defaultValue: 'hsl(219, 79%, 66%)',
    xChannel: 'hue',
    yChannel: 'saturation'
  },
  argTypes: {
    xChannel: {
      control: 'select',
      options: ['hue', 'saturation', 'lightness']
    },
    yChannel: {
      control: 'select',
      options: ['hue', 'saturation', 'lightness']
    }
  }
}`,...(y=(f=s.parameters)==null?void 0:f.docs)==null?void 0:y.source}}};var b,S,A;l.parameters={...l.parameters,docs:{...(b=l.parameters)==null?void 0:b.docs,source:{originalSource:`{
  render: ColorAreaExample.render,
  args: {
    defaultValue: 'hsb(219, 79%, 66%)',
    xChannel: 'hue',
    yChannel: 'saturation'
  },
  argTypes: {
    xChannel: {
      control: 'select',
      options: ['hue', 'saturation', 'brightness']
    },
    yChannel: {
      control: 'select',
      options: ['hue', 'saturation', 'brightness']
    }
  }
}`,...(A=(S=l.parameters)==null?void 0:S.docs)==null?void 0:A.source}}};const z=["ColorAreaExampleRender","ColorAreaExample","ColorAreaHSL","ColorAreaHSB"];export{o as ColorAreaExample,T as ColorAreaExampleRender,l as ColorAreaHSB,s as ColorAreaHSL,z as __namedExportsOrder,q as default};
