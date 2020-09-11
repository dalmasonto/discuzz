import React, { Component } from 'react';

import { IonContent, IonSplitPane, IonHeader, IonToolbar, IonMenu, IonTitle, IonList, IonItem, IonLabel, IonButton, IonGrid, IonRow, IonCol } from '@ionic/react'
import { IoIosHome, IoIosLogIn, IoIosNotifications, IoIosHeart, IoIosPerson, IoIosLogOut, IoIosReorder } from 'react-icons/io';


import { Route, Switch, Redirect } from 'react-router-dom';
import { IonReactRouter } from '@ionic/react-router';
import { IonRouterOutlet } from '@ionic/react'

import Home from '../pages/Home';
import Discuzz from '../pages/Discuzz'
import Error from '../pages/Error';

export default class Routerr extends Component {


  state = {
    loggedIn: false,
  }


  render() {



    return (
      <>
        <IonSplitPane contentId="main" className="new-pane" when="xs" disabled="true" color="">
          <IonMenu contentId="main" menuId="homeMenu" side="start" type="overlay" mode="ios" color="">
            <IonHeader>
              <IonToolbar>
                <IonTitle> The Blogger </IonTitle>
              </IonToolbar>
            </IonHeader>
            <IonContent className="menu-center" color="">
              <IonList color="dark">

                <IonItem routerLink="/home" color="">
                  <IoIosHome className="nav-icon" slot="start" />
                  <IonLabel>
                    Home
                </IonLabel>
                </IonItem>



                <IonItem routerLink="/profile/" color="">
                  <IoIosPerson slot="start" className="nav-icon" />
                  <IonLabel>
                    Profile
                        </IonLabel>
                </IonItem>

                <IonItem routerLink="/notifications" routerDirection="forward" color="">
                  <IoIosNotifications slot="start" className="nav-icon" />
                  <IonLabel>
                    Notifications
                        </IonLabel>
                </IonItem>

                <IonItem routerLink="/favourites/" color="">
                  <IoIosHeart slot="start" className="nav-icon text-danger danger" color="danger" />
                  <IonLabel>
                    Favourites
                        </IonLabel>
                </IonItem>

                <IonItem color="">
                  <IoIosLogOut slot="start" className="nav-icon" />
                  <IonGrid className="ion-no-padding ion-no-margin">
                    <IonRow className="ion-no-padding ion-no-margin">
                      <IonCol className="ion-no-padding ion-no-margin">
                        <IonButton fill="solid" expand="block" onclick={this.logoutuser}>

                          <IonLabel className="ion-padding">
                            Logout
                                </IonLabel>

                        </IonButton>
                      </IonCol>
                    </IonRow>
                  </IonGrid>
                </IonItem>



                <IonItem routerLink="/login" color="">
                  <IoIosLogIn className="nav-icon" slot="start" />
                  <IonLabel>
                    Login | Sign Up
                        </IonLabel>
                </IonItem>




                <IonItem routerLink="/categories" color="">
                  <IoIosReorder slot="start" className="nav-icon" />
                  <IonLabel>
                    Categories
                  </IonLabel>
                </IonItem>



              </IonList>
            </IonContent>
          </IonMenu>



          <IonReactRouter>
            <IonRouterOutlet id="main">

              <Switch>

                <Route exact path="/home" component={Home} />
                <Route exact path="/" render={() => <Redirect to="/home" />} />
                <Route exact path='/login/' component={Home} />
                <Route exact path='/favourites/' component={Home} />
                <Route exact path='/notifications/' component={Home} />
                <Route exact path='/profile/' component={Home} />
                <Route exact path='/categories/' component={Home} />
                <Route exact path='/discuzz/:view/' component={Discuzz} />
                <Route component={Error} />

              </Switch>

            </IonRouterOutlet>
          </IonReactRouter>
        </IonSplitPane>
      </>
    )
  }
}

