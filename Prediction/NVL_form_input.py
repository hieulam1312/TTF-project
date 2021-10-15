import streamlit as st
r1,r2,r3,r4,r5=st.columns((1,1,1,2,2))
if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter(increment_value=0):
    st.session_state.count += increment_value

def decrement_counter(decrement_value=0):
    st.session_state.count -= decrement_value
c1,c2,c3,c4,c5=st.columns((1,1,1,2,2))
with c1:
    st.button('Thêm dòng', on_click=increment_counter,
        kwargs=dict(increment_value=5))
with c2:
    st.button('Giảm dòng', on_click=decrement_counter,
        kwargs=dict(decrement_value=1))
with c4:
    st.write('Tổng số dòng = ', st.session_state.count)
h=st.session_state.count

with r1:
        a=[st.text_input('Dày',)]
        for n in range(st.session_state.count):
            a.append(st.text_input(label='', key=f'Question {n}'))
with r2:
        b=[st.text_input('Rộng',)]
        for nr in range(st.session_state.count):
            b.append(st.text_input(label='', key=f'2`1 {nr}'))
with r3:
        c=[st.text_input('Dài',)]
        for ng in range(st.session_state.count):
            c.append(st.text_input(label='', key=f'dfuestion {ng}'))
with r4:
        d= [st.number_input('Số thanh',step=1)]
        for ngg in range(st.session_state.count):
            d.append(st.number_input(label='', key=f'Quesdfgtion {ngg}',step=  1))
with r5: 
    if a[0]:
        st.markdown("")
        g=[st.write("Số lượng:\n",d[0])]
        hh=[st.write('Số khối',(int(a[0])*int(b[0])*int(c[0])*int(d[0]))/1000000)]
        st.markdown("")


        for nr in range(st.session_state.count):
            if not a[nr]:
                g.append(st.write("Số lượng:\n",d[nr]))
                st.write('Số khối',0)
                st.markdown("")

 
            elif a[nr]:   
                g.append(st.write("Số lượng:\n",d[nr]))
                hh.append(st.write('Số khối',(int(a[nr])*int(b[nr])*int(c[nr])*d[nr])/1000000))
                st.markdown("")

                
    
a
b
c
d
g
hh


# submitted = st.form_submit_button("Submit")
