import React, { Component } from 'react'

import Navbar from '../components/Navbar'
import { Applicationcontext } from '../providers/Application'

import Question from '../components/Question'
import Footer from '../components/Footer'
import { IonContent, IonSpinner, IonLoading } from '@ionic/react'

export default class Home extends Component {

  static contextType = Applicationcontext

  constructor(){
    super()
  }

  state = {
    state_quizes: [],
    state_sorted_quizes: [],
    state_loading: true,
  }

  // async componentWillMount(){
  //   const { questions, sorted_questions, loading } = this.context;
  //   console.log('THE QUIZES AT HOME ARE', questions)
  //   this.setState({
  //     state_quizes: questions,
  //     state_sorted_quizes: sorted_questions,
  //     state_loading: loading
  //   })
  //   console.log('home data', this.state)
  // }

  // UNSAFE_componentWillMount


  render() {
    const { questions, sorted_questions, loading } = this.context;


    const search_text = React.createRef()
    const search_params = React.createRef()

    const search = () => {
      let params
      let text = search_text.current.value
      if(search_params.current.value === undefined || search_params.current === null){
        params = '';
      }
      else{
        params = search_params.current.value
      }
      const search_regex = RegExp(text, 'gi');
      let searched_quizes = this.state.state_quizes.filter(quiz => quiz.topic.match(search_regex))
      this.setState({
        state_sorted_quizes: searched_quizes
      })


    }

    return (
      <>
        <Navbar />
        <IonContent fullscreen={true} className="ion-margin-bottom mb-2 pb-5">
        {
          loading === true ? 
          (
            <>
            
            <IonLoading message="loading...<br/> please wait " className="" cssClass="primary" isOpen={true} spinner="bubbles" mode="ios"></IonLoading>
            
            </>
          )
          : 
          (
            sorted_questions.map((quiz, index) => {
              return <Question obj={quiz} key={index} />
            })
          )
        }
        <Footer />
        </IonContent>
        
      </>
    )
  }
}
