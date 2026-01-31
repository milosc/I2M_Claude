import{j as e}from"./jsx-runtime-CDt2p4po.js";import{a0 as t,L as i,I as d,Z as p}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";/* empty css               */import"./index-C8NrMXaH.js";const x={title:"React Aria Components/ColorField",argTypes:{colorSpace:{control:"select",options:["rgb","hsl","hsb"]},channel:{control:"select",options:[null,"red","green","blue","hue","saturation","lightness","brightness"]}},component:t},l={render:a=>e.jsxs(t,{...a,validate:r=>(r==null?void 0:r.getChannelValue("red"))===0?"Invalid value":null,children:[e.jsx(i,{children:a.label}),e.jsx(d,{style:{display:"block"}}),e.jsx(p,{})]}),args:{label:"Test",defaultValue:"#f00"}};var o,s,n;l.parameters={...l.parameters,docs:{...(o=l.parameters)==null?void 0:o.docs,source:{originalSource:`{
  render: args => <ColorField {...args} validate={v => v?.getChannelValue('red') === 0 ? 'Invalid value' : null}>
      <Label>{args.label}</Label>
      <Input style={{
      display: 'block'
    }} />
      <FieldError />
    </ColorField>,
  args: {
    label: 'Test',
    defaultValue: '#f00'
  }
}`,...(n=(s=l.parameters)==null?void 0:s.docs)==null?void 0:n.source}}};const C=["ColorFieldExample"];export{l as ColorFieldExample,C as __namedExportsOrder,x as default};
