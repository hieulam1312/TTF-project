import streamlit as st
list=['Dày','Rộng','Dài']
r=st.columns(5)
for i,col in enumerate(r):
        with col:
            if i<=2:
                b=st.text_input(list[i],key=i)
            if i==3:
                sum=0
                # with col
                if st.button('\nCộng 1\n'):
                    st.session_state.count += 1
                if st.button('Trừ 1'):
                    st.session_state.count -= 1

            if i==4:
                st.write("Số lượng:",st.session_state.count)
                st.write('Số khối')