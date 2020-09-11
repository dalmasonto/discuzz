import React, { Component } from 'react'
import { IonToolbar, IonButtons, IonMenuButton, } from '@ionic/react'

export default class componentName extends Component {
  render() {
    return (
      <>
        <IonToolbar mode="ios" color="dark">
            <IonButtons slot="start">
                <IonMenuButton></IonMenuButton>
            </IonButtons>
        </IonToolbar>
      </>
    )
  }
}
