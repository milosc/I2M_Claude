import{j as e}from"./jsx-runtime-CDt2p4po.js";import{T as a,L as c,I as u,_ as F,Z as b,B as r}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";import{c as i}from"./utils-N1pTmi3h.js";import{s as o}from"./index.module-B9nxguEg.js";/* empty css               */import"./index-C8NrMXaH.js";const _={title:"React Aria Components/TextField",component:a},s=()=>e.jsxs(a,{"data-testid":"textfield-example",children:[e.jsx(c,{children:"First name"}),e.jsx(u,{})]}),t=h=>e.jsxs(F,{children:[e.jsxs(a,{className:i(o,"textfieldExample"),name:"email",type:"email",isRequired:!0,...h,children:[e.jsx(c,{children:"Email"}),e.jsx(u,{}),e.jsx(b,{className:i(o,"errorMessage")})]}),e.jsx(r,{type:"submit",children:"Submit"}),e.jsx(r,{type:"reset",children:"Reset"})]});t.story={argTypes:{isInvalid:{control:{type:"boolean"}}},parameters:{description:{data:"Non controlled isInvalid should render the default error message (aka just hit submit and see that it appears). Controlled isInvalid=true should not render the error message div (aka no padding should appear between the input and the buttons)."}}};s.__docgenInfo={description:"",methods:[],displayName:"TextfieldExample"};t.__docgenInfo={description:"",methods:[],displayName:"TextFieldSubmitExample"};var l,m,d;s.parameters={...s.parameters,docs:{...(l=s.parameters)==null?void 0:l.docs,source:{originalSource:`() => {
  return <TextField data-testid="textfield-example">
      <Label>First name</Label>
      <Input />
    </TextField>;
}`,...(d=(m=s.parameters)==null?void 0:m.docs)==null?void 0:d.source}}};var n,p,x;t.parameters={...t.parameters,docs:{...(n=t.parameters)==null?void 0:n.docs,source:{originalSource:`args => {
  return <Form>
      <TextField className={classNames(styles, 'textfieldExample')} name="email" type="email" isRequired {...args}>
        <Label>Email</Label>
        <Input />
        <FieldError className={classNames(styles, 'errorMessage')} />
      </TextField>
      <Button type="submit">Submit</Button>
      <Button type="reset">Reset</Button>
    </Form>;
}`,...(x=(p=t.parameters)==null?void 0:p.docs)==null?void 0:x.source}}};const S=["TextfieldExample","TextFieldSubmitExample"];export{t as TextFieldSubmitExample,s as TextfieldExample,S as __namedExportsOrder,_ as default};
