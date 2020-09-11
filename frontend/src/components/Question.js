import React, { Component } from 'react'
import { IonCard, IonCardHeader, IonCardTitle, IonCardSubtitle, IonTitle, IonCardContent, IonAvatar, IonLabel, IonChip } from '@ionic/react'

export default class Question extends Component {
  render() {
    const obj = this.props.obj
    const avatar_url = `http://127.0.0.1:8000${obj.admin.userextension.profile_pic}`
    return (
      <>
        <IonCard>
          <IonCardHeader>
            <IonCardTitle> {obj.topic}, {obj.subtopic} </IonCardTitle>
          </IonCardHeader>
          <IonCardContent>
            <h2 className="text-center h2"> Description </h2>
            <p className=""> {obj.description} </p>
            <h2> Question </h2>
            <p className=""> {obj.question} </p>
              <h2> Discussion code </h2>
            <p className="card-text"> <span className="code">{obj.discussionCode}</span></p>

            <div className="">
              <p className="ion-no-padding">
                <span className="float-right">
                  by
                <IonChip color="primary">
                    <IonAvatar>
                      <img src={avatar_url} alt={obj.admin.first_name} />
                    </IonAvatar>
                    <IonLabel>
                      {obj.admin.username} <span className="text-warning">{obj.discuzz_set.length} replies </span>
                    </IonLabel>
                  </IonChip>
                </span>
              </p>
            </div>
          </IonCardContent>
        </IonCard>
      </>
    )
  }
}
