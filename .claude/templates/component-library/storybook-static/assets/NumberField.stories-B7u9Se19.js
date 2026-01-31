import{j as e}from"./jsx-runtime-CDt2p4po.js";import{aQ as n,L as p,al as x,B as a,I as f,Z as b}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{r as h}from"./index-GiUgBvb1.js";/* empty css               */import"./index-C8NrMXaH.js";const S={title:"React Aria Components/NumberField",component:n},l={args:{defaultValue:0,minValue:0,maxValue:100,step:1,formatOptions:{style:"currency",currency:"USD"},isWheelDisabled:!1},render:r=>e.jsxs(n,{...r,validate:t=>t&1?"Invalid value":null,children:[e.jsx(p,{children:"Test"}),e.jsxs(x,{style:{display:"flex"},children:[e.jsx(a,{slot:"decrement",children:"-"}),e.jsx(f,{}),e.jsx(a,{slot:"increment",children:"+"})]}),e.jsx(b,{})]})};function V(r){const[t,y]=h.useState(r.defaultValue);return e.jsxs(n,{...r,validate:j=>j&1?"Invalid value":null,value:t,onChange:y,children:[e.jsx(p,{children:"Test"}),e.jsxs(x,{style:{display:"flex"},children:[e.jsx(a,{slot:"decrement",children:"-"}),e.jsx(f,{}),e.jsx(a,{slot:"increment",children:"+"})]}),e.jsx(b,{})]})}const s={args:{defaultValue:0,minValue:0,maxValue:100,step:1,formatOptions:{style:"currency",currency:"USD"},isWheelDisabled:!1},render:r=>e.jsx(V,{...r})};var o,i,u;l.parameters={...l.parameters,docs:{...(o=l.parameters)==null?void 0:o.docs,source:{originalSource:`{
  args: {
    defaultValue: 0,
    minValue: 0,
    maxValue: 100,
    step: 1,
    formatOptions: {
      style: 'currency',
      currency: 'USD'
    },
    isWheelDisabled: false
  },
  render: args => <NumberField {...args} validate={v => v & 1 ? 'Invalid value' : null}>
      <Label>Test</Label>
      <Group style={{
      display: 'flex'
    }}>
        <Button slot="decrement">-</Button>
        <Input />
        <Button slot="increment">+</Button>
      </Group>
      <FieldError />
    </NumberField>
}`,...(u=(i=l.parameters)==null?void 0:i.docs)==null?void 0:u.source}}};var d,m,c;s.parameters={...s.parameters,docs:{...(d=s.parameters)==null?void 0:d.docs,source:{originalSource:`{
  args: {
    defaultValue: 0,
    minValue: 0,
    maxValue: 100,
    step: 1,
    formatOptions: {
      style: 'currency',
      currency: 'USD'
    },
    isWheelDisabled: false
  },
  render: args => <NumberFieldControlled {...args} />
}`,...(c=(m=s.parameters)==null?void 0:m.docs)==null?void 0:c.source}}};const B=["NumberFieldExample","NumberFieldControlledExample"];export{s as NumberFieldControlledExample,l as NumberFieldExample,B as __namedExportsOrder,S as default};
