import {Col, Row} from "react-bootstrap"
import { useState } from 'react' 
import ListGroup from 'react-bootstrap/ListGroup';
import Image from 'react-bootstrap/Image'

export default function ImageViewer() {
    
    const [isImageSelected, setIsImageSelected] = useState(false)
    const [imageFile, setImageFile] = useState("None")
    //const [fileList, setFileList] = useState("Error retrieving files")

    //Temporary list of images until backend connection
    var tempList = ["0.jpeg", "25.jpeg"]

    const handleImageSelection = (file) => {
        setIsImageSelected(true)
        setImageFile(file)
    }
    
    return (    
    <Row>
        {/* // Image selection listgroup */}
        <Col className="col-sm-3">
            <ListGroup>
                <label><strong>Select Image</strong></label>
            {tempList.map((item) => (
                <ListGroup.Item
                key={item}
                active={imageFile === item} // Set active state for specific item
                onClick={() => handleImageSelection(item)}
                >
                {item}
                </ListGroup.Item>
            ))}
            </ListGroup>
        </Col> 
        {/* Renders image if an image is selected */}
        <Col>
            {isImageSelected ? (            
            <Image
                src={require("../../../cubesat-backend/cubesat_images/img/" + imageFile)}
                alt="DIDNT LOAD"
                fluid
                rounded
                width = {500}
            />) : null}
        </Col>
    </Row>
     )
    
    
}