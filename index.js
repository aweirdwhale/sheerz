const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();
const port = 3000;

const { exec } = require('child_process');

const pythonScript = path.join(__dirname, 'script/sheepCounter.py');
const pythonOuptut = "./script/output/";
const command = `python3 ${pythonScript} -i ${path.join(__dirname, 'uploads/*')} -o ${pythonOuptut} -obj sheep`;




const token = ""
// Configure multer pour stocker les fichiers uploadés


const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, 'uploads')); // Utilise path.join pour assurer la bonne résolution du chemin
  },
  filename: function (req, file, cb) {
    cb(null, "input" + path.extname(file.originalname));
  }
});

const upload = multer({ storage: storage });




// Route pour gérer le téléchargement de fichiers
app.post('/sheerz', upload.single('image'), (req, res) => {
    // check headers
    let headers = req.headers;
    if (headers['sheerz-auth'] !== token) {
        return res.status(401)
                  .send('Clé API invalide.');
    }
    

    // 'image' doit correspondre au nom du champ de fichier dans la requête
    if (!req.file) {
        return res.status(400)
                .send('Aucun fichier n\'a été téléchargé.');
    }

    

    exec(command, (error, stdout, stderr) => {
        if (error) {
            res.status(500).send('Erreur lors de l\'exécution du script.' + error);
            return;
        }
    
        // if (stderr) {
        //     res.status(500).send('Erreur lors de l\'exécution du script.' + stderr);
        //     return;
        // }
    
        try {
            
            res.status(200)
            //    .sendFile(path.join(__dirname, 'script/output/verbose.json'))
               .sendFile(path.join(__dirname, 'script/output/output.jpg'));
            //    .json("./script/output/verbose.json")
            //    .on('finish', () => {
            //        // Supprimer le fichier après l'envoi
            //        fs.unlinkSync(path.join(__dirname, 'uploads', req.file.filename));
            //        fs.unlinkSync(path.join(__dirname, 'script/output/verbose.json'));
            //          fs.unlinkSync(path.join(__dirname, 'script/output/output.jpg'));
            //    });

        } catch (parseError) {

            res.status(500)
               .send('Erreur lors de la lecture du fichier JSON.');

        }
    });

});

app.listen(port, () => {
  console.log(`Serveur à l'écoute sur le port ${port}`);
});


function use(res) {
    


}