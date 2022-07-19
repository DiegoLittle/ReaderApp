//
//  SlideMenu.swift
//  ReaderApp
//
//  Created by Diego Little on 4/30/22.
//

import Foundation
import SwiftUI
import WebKit

struct MenuView: View{
    var sections:[section]
    var webview:WKWebView
    var browser:Browser
    var bounds = UIScreen.main.bounds
    var width = UIScreen.screenWidth
    var height = UIScreen.screenHeight
    var newSafeArea = UIEdgeInsets()
    var navigationController:UINavigationController
    
    func getHeight() -> CGFloat{
        let screenHeight = UIScreen.main.bounds.size.height
        let topBarBottom = self.navigationController.navigationBar.frame.maxY
        let toolbarTop = self.navigationController.toolbar.frame.origin.y
        let originalHeight = screenHeight - toolbarTop
        return self.height - originalHeight-topBarBottom
    }
//    var bottom = UIApplication.shared.keyWindow?.safeAreaInsets.bottom
//    var top = UIApplication.shared.keyWindow?.safeAreaInsets.top
    
    var body: some View{
        
        VStack{
            Color(red: 68 / 255, green: 68 / 255, blue: 68 / 255)
                .overlay(
                    VStack(alignment:.leading) {
                        Text("Contents")
                            .font(.title3)
                            .fontWeight(Font.Weight.semibold)
                            .frame(alignment:.leading)
                            .padding([.leading,.top])
                        ScrollView{
                            VStack{
                            ForEach(sections){ section in
                                VStack{
//                                    Text(subsection.section_title)
                                    Button(action:{
                                            self.webview.evaluateJavaScript(
                                                "document.querySelector('"+section.selector+"').scrollIntoView({behavior: 'smooth'});"
                                            )
                                        browser.closeMenu()

                                        
                                    }){

                                        Text(section.section_title)
                                            .fontWeight(Font.Weight.semibold)
                                            .font(.system(size: 20))
                                            .foregroundColor(Color.white)
                                            .frame(maxWidth: .infinity ,alignment:.leading)
                                            .padding([.leading],5)
                                    }
                                    ForEach(section.subsections){ subsection in
                                        Button(action:{
                                            print(subsection.selector)
                                                self.webview.evaluateJavaScript(
                                                    "document.querySelector('"+subsection.selector+"').scrollIntoView({behavior: 'smooth'});"
                                                )
                                            browser.closeMenu()

                                            
                                        }){

//                                            Text(section.section_title)
                                            Text(subsection.section_title)
                                                .frame(maxWidth: .infinity, alignment:.leading)
                                                .padding([.leading],5)
                                                .foregroundColor(Theme.Color.gray100)
                                                .padding([.vertical],1.5)
                                        }

                                            
                                    }
                                }
                                .padding([.vertical],7.5)
                            }
                            }
                            .padding([.leading],5)
                    }
//                        Text("Example").font(.title).foregroundColor(.white)
                        Spacer()
                }
                )
//            Spacer()
        }.cornerRadius(10)
            .frame(width: 250, height: getHeight())
            .padding([.top],self.navigationController.navigationBar.frame.height)
//        ZStack{
//            VStack(alignment: .leading){
//                Text("Table of Contents").padding().foregroundColor(Color.white)
//                Text("Table of Contents").padding().foregroundColor(Color.white)
//            }
//            Color(red: 68 / 255, green: 68 / 255, blue: 68 / 255)
//
//            Spacer()
//        }.cornerRadius(10)
//            .frame(width:200,height:height)

    }
}
