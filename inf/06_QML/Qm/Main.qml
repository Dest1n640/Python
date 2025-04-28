import QtQuick
import QtQuick.Window 2.15

Window {
    width: 400
    height: 600
    visible: true
    title: "Человечек из фигур"

    Rectangle {
        anchors.fill: parent
        color: "white"

        // Голова
        Rectangle {
            width: 60
            height: 60
            color: "peachpuff"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 50
        }

        // Тело
        Rectangle {
            width: 30
            height: 100
            color: "blue"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 110
            radius: 10
        }

        // Левая рука
        Rectangle {
            width: 15
            height: 70
            color: "green"
            anchors.right: parent.horizontalCenter
            anchors.rightMargin: 20
            anchors.top: parent.top
            anchors.topMargin: 110
            rotation: -20
        }

        // Правая рука
        Rectangle {
            width: 15
            height: 70
            color: "green"
            anchors.left: parent.horizontalCenter
            anchors.leftMargin: 20
            anchors.top: parent.top
            anchors.topMargin: 110
            rotation: 20
        }

        // Левая нога
        Rectangle {
            width: 15
            height: 80
            color: "brown"
            anchors.right: parent.horizontalCenter
            anchors.rightMargin: 10
            anchors.top: parent.top
            anchors.topMargin: 210
            rotation: -10
        }

        // Правая нога
        Rectangle {
            width: 15
            height: 80
            color: "brown"
            anchors.left: parent.horizontalCenter
            anchors.leftMargin: 10
            anchors.top: parent.top
            anchors.topMargin: 210
            rotation: 10
        }
    }
}
