import{j as e}from"./jsx-runtime-CDt2p4po.js";import{a as x}from"./index-B-lxVbXh.js";import{_ as m,T as o,L as i,I as a,f as c,B as n,g as u,P as h,b as j,aq as t}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";/* empty css               */import"./v4-CtRu48qb.js";import"./index-C8NrMXaH.js";const C={title:"React Aria Components/Form",component:m},s=()=>e.jsxs(m,{"aria-label":"Shipping information",onSubmit:r=>{x("onSubmit")(Object.fromEntries(new FormData(r.target).entries())),r.preventDefault()},children:[e.jsxs(o,{children:[e.jsx(i,{children:"Address"}),e.jsx(a,{name:"streetAddress",type:"text",id:"streetAddress",autoComplete:"shipping street-address"})]}),e.jsxs(o,{children:[e.jsx(i,{children:"City"}),e.jsx(a,{name:"city",type:"text",id:"city",autoComplete:"shipping address-level2"})]}),e.jsxs(o,{children:[e.jsx(i,{children:"State"}),e.jsx(a,{name:"state",type:"text",id:"state",autoComplete:"shipping address-level1"})]}),e.jsxs(o,{children:[e.jsx(i,{children:"Zip"}),e.jsx(a,{name:"city",type:"text",id:"city",autoComplete:"shipping postal-code"})]}),e.jsxs(c,{name:"country",id:"country",autoComplete:"shipping country",children:[e.jsx(i,{children:"Country"}),e.jsxs(n,{children:[e.jsx(u,{}),e.jsx("span",{"aria-hidden":"true",children:"▼"})]}),e.jsx(h,{children:e.jsxs(j,{children:[e.jsx(t,{children:"Greece"}),e.jsx(t,{children:"Italy"}),e.jsx(t,{children:"Spain"}),e.jsx(t,{children:"Mexico"}),e.jsx(t,{children:"Canada"}),e.jsx(t,{children:"United States"})]})})]}),e.jsx(n,{type:"submit",children:"Submit"})]});s.__docgenInfo={description:"",methods:[],displayName:"FormAutoFillExample"};var l,d,p;s.parameters={...s.parameters,docs:{...(l=s.parameters)==null?void 0:l.docs,source:{originalSource:`() => {
  return <Form aria-label="Shipping information" onSubmit={e => {
    action('onSubmit')(Object.fromEntries(new FormData(e.target as HTMLFormElement).entries()));
    e.preventDefault();
  }}>
      <TextField>
        <Label>Address</Label>
        <Input name="streetAddress" type="text" id="streetAddress" autoComplete="shipping street-address" />
      </TextField>
      <TextField>
        <Label>City</Label>
        <Input name="city" type="text" id="city" autoComplete="shipping address-level2" />
      </TextField>
      <TextField>
        <Label>State</Label>
        <Input name="state" type="text" id="state" autoComplete="shipping address-level1" />
      </TextField>
      <TextField>
        <Label>Zip</Label>
        <Input name="city" type="text" id="city" autoComplete="shipping postal-code" />
      </TextField>
      <Select name="country" id="country" autoComplete="shipping country">
        <Label>Country</Label>
        <Button>
          <SelectValue />
          <span aria-hidden="true">▼</span>
        </Button>
        <Popover>
          <ListBox>
            <ListBoxItem>Greece</ListBoxItem>
            <ListBoxItem>Italy</ListBoxItem>
            <ListBoxItem>Spain</ListBoxItem>
            <ListBoxItem>Mexico</ListBoxItem>
            <ListBoxItem>Canada</ListBoxItem>
            <ListBoxItem>United States</ListBoxItem>
          </ListBox>
        </Popover>
      </Select>
      <Button type="submit">Submit</Button>
    </Form>;
}`,...(p=(d=s.parameters)==null?void 0:d.docs)==null?void 0:p.source}}};const f=["FormAutoFillExample"];export{s as FormAutoFillExample,f as __namedExportsOrder,C as default};
