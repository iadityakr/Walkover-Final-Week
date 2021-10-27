pipeline{
    agent none
    stages{
        stage('Stage'){
            agent any
            steps{
                echo "Creating Backup ..."
                echo "Build number is ${currentBuild.number}"
                echo "Previous Build number is ${currentBuild.previousBuild.number}"
                sh "sudo zip -r production${currentBuild.number}.zip /home/ubuntu/production "
                sh "sudo mv production${currentBuild.number}.zip /home/ubuntu/backup"
                // sh "sudo rm -f /home/ubuntu/backup/production${currentBuild.previousBuild.number}.zip"
            }       
        }
        stage('Build'){
            agent any
            steps{
                    sh "sudo rm -rf /home/ubuntu/production/templates"
                    sh "sudo rm -rf /home/ubuntu/production/myenv"
                    sh "sudo rm -rf /home/ubuntu/production/__pycache__"
                    sh "sudo mv * /home/ubuntu/production/"
            }
        }
        
        stage('Deploy'){
            agent any
            steps{
                sh "sudo systemctl restart myproject"
                sh "sudo systemctl restart nginx"
        }
    }
}
}