import QtQuick 

Window {
  width: 640
  height: 480
  visible: true
  title: qsTr("Hello world")

  Rectangle{
    id:rect 
    width: 300
    height: 300
    border.width: 3
    border.color: "gray"
    anchors:centerIn: parent
  }
}
